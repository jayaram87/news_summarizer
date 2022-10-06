import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from src.exception import CustomException
from src.constants import *

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

class NewsCollection():
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """quits the driver object
        """
        try:
            self.driver.quit()
        except CustomException as e:
            raise CustomException(e, sys) from e

    def url_page(self, url):
        """
        opens the url page
        """
        try:
            self.driver.maximize_window()
            self.driver.get(url)
            self.driver.implicitly_wait(30)
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') # scroll to the top of the page
        except CustomException as e:
            raise CustomException(e, sys) from e

a = NewsCollection()
a.url_page('google.com')
