from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_webdriver
from selenium.webdriver.common.by import By


class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.browser = make_webdriver()

    def tearDown(self):
        super().tearDown()
        self.browser.quit()

    @staticmethod
    def get_by_placeholder(web_element, placeholder):
        return web_element.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]')