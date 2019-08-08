from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import sys, os, re, json
from datetime import datetime
import pickle
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
import numpy as np
import time
import argparse   #Command line option and argument parsing (phân tích các tham số và tùy chọn trên ... )


# sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from neo4jDir.createneo4j import ImportNeo4j


class Livestream:
    LOGIN_URL = 'https://www.facebook.com/login.php?login_attempt=1&lwv=111'

    def __init__(self, login, password):
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=./chrome")

        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)   #Thêm 1 tùy chọn thử nghiệm được truyền cho chrome

        self.driver = webdriver.Chrome(executable_path=r'./chromedriver', options=options)

        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get('https://www.facebook.com')
        # self.login(login, password)
        # self.load_cookie('cookies.pkl')
        if os.path.exists('cookies.pkl'):
            self.load_cookie('cookies.pkl')
        else:
            self.login(login, password)

    def login(self, login, password):
        self.driver.get(self.LOGIN_URL)

        # wait for the login page to load
        self.wait.until(EC.visibility_of_element_located( (By.ID, "email") ))

        self.driver.find_element_by_id('email').send_keys(login)
        self.driver.find_element_by_id('pass').send_keys(password)
        self.driver.find_element_by_id('loginbutton').click()

        # wait for the main page to load
        self.wait.until(EC.visibility_of_element_located( (By.XPATH, "div[data-click='profile_icon']")  )) #thay xpath bằng By.CSS_SELLECTOR, doi cho den khi trong trang load có thẻ hoặc đường dẫn kia

        facebook_cookies = self.driver.get_cookies()
        # print(facebook_cookies)
        # Nếu file đã tồn tại, thì ghi đè nội dung của file đó, nếu không thì tạo một file mới
        with open("cookies.pkl", "wb") as fd:
            pickle.dump(facebook_cookies, fd)   #pickling cookies vào file cookies đã mở

        # self.driver.quit()

        # return cookies

    def load_cookie(self, path):
        # Mở file trong chế độ ghi trong định dạng nhị phân.
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)  #unpickling tạo lại đối tượng cookies từ chuỗi file cookiesfile
            for cookie in cookies:
                # Check xem trong cookie co key expry khong, neu co thi xoa di
                if 'expiry' in cookie:
                    del cookie['expiry']
                self.driver.add_cookie(cookie)  #add cookie vao browser

    def _get_amount_image_list(self, select_elem):    #Tìm kiếm và trả về object các phần tử element
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, select_elem)))
        return self.driver.find_elements_by_css_selector(select_elem)

    def crawl_get_list_image_tagged(self, fb_id):
        # navigate to "image tagged" page
        try:
            self.driver.get("https://www.facebook.com/%s/photos_of" % fb_id)   #Chuyển thành photos_all sẽ được nhiều ảnh hơn do đây là ảnh fb_id đăng

            # continuous scroll until no more new images loaded
            num_of_loaded_images = len(self._get_amount_image_list("li.fbPhotoStarGridElement"))  #Đếm số ảnh bằng cách đếm số thẻ  <li> có class tên fb...
            # print('%s' % fb_id + ': ' + str(num_of_loaded_images) + ' ảnh' )
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Chạy javascript để cuộn hết auto cuộn nên phải dừng lại
                try:
                    self.wait.until(
                        lambda drive: len(    #Hàm ẩn danh lambda tham số tên driver #Hàm ẩn danh chạy luôn
                            self._get_amount_image_list("li.fbPhotoStarGridElement")) > num_of_loaded_images)   #
                    # print("chỗ này chạy %s" %num_of_loaded_images)
                    num_of_loaded_images = len(self._get_amount_image_list("li.fbPhotoStarGridElement"))

                except TimeoutException:
                    # print("chỗ này dừng %s" %num_of_loaded_images)

                    break #no more images loader
            # print('%s' % fb_id + ': ' + str(num_of_loaded_images) + ' ảnh')
            return [image for image in self._get_amount_image_list("li.fbPhotoStarGridElement")]  #Trả về mảng object image của selenium có chứa element li.fb...
        except TimeoutException:
            print('Time out-here!')
            return

    def crawl_get_image_tagged(self, fb_id):    #Crawl số tag trong ảnh
        list_all_images = self.crawl_get_list_image_tagged(fb_id)

        if list_all_images is not None:
            ts = time.time()
            time_allow = 150076800   #utime
            for image in list_all_images:
                image_fb_id = image.get_attribute('data-fbid')   #Lấy id là data-fb-id, dữ liệu ảnh, id của ảnh đó
                href = str(image.find_element_by_xpath('.//a').get_attribute('href'))  #Lấy link của ảnh
                if 'videos' in href.split('/'):          #Nếu là video thì bỏ qua
                    continue
                try:

                    image.click()  #Click vào ảnh
                    self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.photoTagLink')))

                    img_time = self.driver.find_element_by_id(
                        'fbPhotoSnowliftTimestampAudienceContainer').find_element_by_css_selector('abbr').get_attribute(
                        'data-utime')
                    if img_time is not None and int(img_time) - ts > time_allow:  #Ảnh cũ quá thì thôi không lấy nữa
                        continue

                    list_tag = self.driver.find_elements_by_css_selector('.photoTagLink')
                    print(len(list_tag))
                    if len(list_tag) > 4:
                        self.driver.find_element_by_xpath('//*[@id="photos_snowlift"]/div[2]/div/a').click()
                        continue
                    for tag in list_tag:
                        fb_id = tag.find_element_by_css_selector('div.fbPhotosPhotoTagboxBase').get_attribute('id')
                        fb_id = re.match(r'.*tag:(.*)$', fb_id).group(1)     #Regular expression  tag:100004287608545

                        element = tag.find_element_by_css_selector(
                            'div.fbPhotosPhotoTagboxBase .borderTagBox').screenshot_as_png
                        # print(element)
                        im = Image.open(BytesIO(element))  # uses PIL library to open image in memory
                        # im.show()
                        im.save(os.path.join('images', '%s_%s.png' % (fb_id, image_fb_id))) #Đã tồn tại thì ghi đè

                    # When finish => Click "X" to close and continue click other images
                    self.driver.find_element_by_xpath('//*[@id="photos_snowlift"]/div[2]/div/a').click()
                except WebDriverException:
                    continue

    def get_friend_list(self, fb_id):
        self.driver.get('https://fb.com/%s/friends' % fb_id)
        num_of_loaded_images = len(self._get_amount_image_list("li._698"))
        # print(self._get_amount_image_list('li._698'))
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: len(self._get_amount_image_list("li._698")) > num_of_loaded_images)
                num_of_loaded_images = len(self._get_amount_image_list("li._698"))
            except TimeoutException:
                break
        friend_elements = self.driver.find_elements_by_class_name("_698")
        friend_list = []
        for elem in friend_elements:
            friend = elem.find_element_by_xpath(".//div/a") # trả về thông tin trong thẻ a
            friend_link = friend.get_attribute('href')
            # print(friend_link)
            fb_id = str(friend_link)[25:-32].replace('profile.php?id=', '') #fb_id của đối tươnng
            # print(fb_id)
            if fb_id == '' or fb_id is None:
                continue
            friend_list.append(fb_id)
        with open('friend_list.pkl', 'wb') as f:
            pickle.dump(friend_list, f)
        return friend_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='facebook image crawler')
    # general
    parser.add_argument('--fb_ids', default='fb_ids.txt', help='path to load list facebook id.')
    parser.add_argument('--craw_from_file', type=bool, default=False, help='crawl from a list of fb ids or from friend '
                                                                           'list of an account')
    args = parser.parse_args()

    crawler = Livestream(login="hunga1k15tv9@gmail.com", password="tieuquy@128")

    if args.craw_from_file:
        assert os.path.exists(args.fb_ids), '%s is not exists'%args.fb_ids #Assertion kiểm tra sự tồn tại của fb_ids   assert bieu_thuc[, cac_tham_so], fb_ids phải trùng với tên arg
        with open('fb_ids.txt', 'r') as f:
            while True:
                id = f.readline().replace('\n', '')
                if id is None or id == '':
                    print('here')
                    break
                try:
                    crawler.crawl_get_image_tagged(id)
                except Exception as e:
                    print(e)
                    continue
    else:
        friend_list_fb_id = crawler.get_friend_list('100029295734811')
        if friend_list_fb_id is not None and len(friend_list_fb_id) > 0:
            for fb_id in friend_list_fb_id:
                crawler.crawl_get_image_tagged(fb_id)