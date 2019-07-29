from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import sys, os, re, json
from datetime import datetime
import pickle
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
import numpy as np
import time

# sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from neo4jDir.createneo4j import ImportNeo4j


class Livestream:
    LOGIN_URL = 'https://www.facebook.com/login.php?login_attempt=1&lwv=111'

    def __init__(self, login, password):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-data-dir=./chrome")

        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(executable_path=r'./chromedriver', chrome_options=chrome_options)

        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get('https://www.facebook.com')
	if not os.exist('cookies.pkl'):
            self.login(login, password)
	else:
	    self.load_cookie('cookies.pkl')

    def login(self, login, password):
        self.driver.get(self.LOGIN_URL)

        # wait for the login page to load
        self.wait.until(EC.visibility_of_element_located((By.ID, "email")))

        self.driver.find_element_by_id('email').send_keys(login)
        self.driver.find_element_by_id('pass').send_keys(password)
        self.driver.find_element_by_id('loginbutton').click()

        # wait for the main page to load
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-click='profile_icon']")))

        facebook_cookies = self.driver.get_cookies()

        with open("cookies.pkl", "wb") as fd:
            pickle.dump(facebook_cookies, fd)

        # self.driver.quit()

        # return cookies

    def load_cookie(self, path):
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def _get_amount_image_list(self, select_elem):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, select_elem)))
        return self.driver.find_elements_by_css_selector(select_elem)

    def crawl_get_list_image_tagged(self, fb_id):
        # navigate to "image tagged" page
        self.driver.get("https://www.facebook.com/%s/photos_of"%fb_id)

        # continuous scroll until no more new friends loaded
        num_of_loaded_images = len(self._get_amount_image_list("li.fbPhotoStarGridElement"))

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: len(self._get_amount_image_list("li.fbPhotoStarGridElement")) > num_of_loaded_images)
                num_of_loaded_images = len(self._get_amount_image_list("li.fbPhotoStarGridElement"))
            except TimeoutException:
                break  # no more friends loaded

        return [image for image in self._get_amount_image_list("li.fbPhotoStarGridElement")]

    def crawl_get_image_tagged(self, crawl_id):
        list_all_images = self.crawl_get_list_image_tagged(crawl_id)

        ts = time.time()
        time_allow = 150076800 # Five year
        for image in list_all_images:
            image_fb_id = image.get_attribute('data-fbid')
            href = str(image.find_element_by_xpath('.//a').get_attribute('href'))
            if 'videos' in href.split('/'):
                continue
            try:
                # list_current_images_id.append(image_fb_id)
                image.click()
                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.photoTagLink')))

                img_time = self.driver.find_element_by_id('fbPhotoSnowliftTimestampAudienceContainer').find_element_by_css_selector('abbr').get_attribute('data-utime')
                if img_time is not None and int(img_time)-ts>time_allow:
                    continue

                list_tag = self.driver.find_elements_by_css_selector('.photoTagLink')
                for tag in list_tag:
                    fb_id = tag.find_element_by_css_selector('div.fbPhotosPhotoTagboxBase').get_attribute('id')
                    fb_id = re.match(r'.*tag:(.*)$', fb_id).group(1)

                    element = tag.find_element_by_css_selector(
                        'div.fbPhotosPhotoTagboxBase .borderTagBox').screenshot_as_png
                    im = Image.open(BytesIO(element))  # uses PIL library to open image in memory
                    im.save(os.path.join('images', '%s_%s.png'%(fb_id, image_fb_id)))
                # When finish => Click "X" to close and continue click other images
                self.driver.find_element_by_xpath('//*[@id="photos_snowlift"]/div[2]/div/a').click()
            except WebDriverException:
                continue

    def get_friend_list(self, fb_id):
        self.driver.get('https://fb.com/%s/friends'%fb_id)
        num_of_loaded_images = len(self._get_amount_image_list("li._698"))
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
            friend = elem.find_element_by_xpath(".//div/a")
            friend_link = friend.get_attribute('href')
            fb_id = str(friend_link)[25:-32].replace('profile.php?id=', '')
            if fb_id == '' or fb_id is None:
                continue
            friend_list.append(fb_id)
        with open('friend_list.pkl', 'wb') as f:
            pickle.dump(friend_list, f)
        return friend_list



if __name__ == '__main__':
    crawler = Livestream(login="nonameforme3896@gmail.com", password="")
    friends = crawler.get_friend_list('doe.jhon.5876')
    if friends is not None and len(friends)>0:
        for friend in friends:
            crawler.crawl_get_image_tagged(friend)
    # with open('fb_ids.txt', 'r') as f:
    #     while True:
    #         id = f.readline().replace('\n', '')
    #         if id is None or id == '':
    #             break
    #         try:
    #             crawler.crawl_get_image_tagged(id)
    #         except Exception:
    #             continue
