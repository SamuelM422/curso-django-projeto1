import time

from tests.functional_tests.authors.base import AuthorsBaseTest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.urls import reverse

class AuthorsRegisterTest(AuthorsBaseTest):
    @staticmethod
    def get_by_placeholder(web_element, placeholder):
        return web_element.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]')

    @staticmethod
    def fill_form_dummy_data(form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(" " * 20)

    def test_empty_first_name_error_test(self):
        self.browser.get(self.live_server_url + reverse('authors:register'))
        form = self.browser.find_element(
            By.XPATH,
            f'/html/body/main/div[2]/form'
        )

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        first_name_field = self.get_by_placeholder(form, 'Ex.: John')
        first_name_field.send_keys('  ')
        first_name_field.send_keys(Keys.ENTER)

        form = self.browser.find_element(
            By.XPATH,
            f'/html/body/main/div[2]/form'
        )

        self.assertIn('Please enter your first name.', form.text)