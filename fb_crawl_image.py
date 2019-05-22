from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import pickle

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("user-data-dir=./chrome")
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome('./chromedriver', )
driver.get('https://fb.com')
wait = WebDriverWait(driver, 10)


def login():
    email = driver.find_element_by_name("email")
    email.send_keys("vulong3896@gmail.com")
    pwd = driver.find_element_by_name("pass")
    pwd.send_keys('l.o.n.g123!@#')
    pwd.submit()


def nav2album():
    driver.get('https://www.facebook.com/chieu.nguyenvan.1447/photos?lst=100005197575955%3A100005594376244%3A1556185180')
    driver.execute_script("window.scrollTo(0,  document.body.scrollHeight);")

def get_photo():
    photos = driver.find_elements_by_xpath("//li[contains(@class, 'fbPhotoStarGridElement') and contains(@class, 'fbPhotoStarGridNonStarred')]")
    for photo in photos:
        a_href = photo.find_element_by_xpath("//a[contains(@class, 'uiMediaThumb') and contains(@class, 'uiMediaThumbMedium')]")
        link = a_href.get_attribute('href')
        print(link)

def _get_amount_image_list():
    wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "li._698")))
    return driver.find_elements_by_css_selector("li._698")

def get_friend_list():
    driver.get('https://fb.com/Longctes/friends')
    num_of_loaded_images = len(_get_amount_image_list())
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            wait.until(lambda driver: len(_get_amount_image_list()) > num_of_loaded_images)
            num_of_loaded_images = len(_get_amount_image_list())
        except TimeoutException:
            break
    friend_elements = driver.find_elements_by_class_name("_698")
    friend_list = []
    for elem in friend_elements:
        friend = elem.find_element_by_xpath(".//div/a")
        friend_link = friend.get_attribute('href')
        print(str(friend_link)[25:-32].replace('profile.php?id=', ''))
        friend_list.append(str(friend_link)[24:-32].replace('profile.php?id=', ''))
    with open('friend_list.pkl', 'wb') as f:
        pickle.dump(friend_list, f)

def load_cookie(path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)

if __name__=='__main__':
    # login()
    # nav2album()
    # get_photo()
    # driver.quit()
    load_cookie('./cookies.pkl')
    get_friend_list()