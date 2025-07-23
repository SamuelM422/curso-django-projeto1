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

    @staticmethod
    def get_form(browser):
        return browser.find_element(
                By.XPATH,
                f'/html/body/main/div[2]/form'
            )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + reverse('authors:register'))
        form = self.get_form(self.browser)

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        callback(form)

        return form

    def test_empty_first_name_error_test(self):
        def callback_first_name(input_form):
            first_name_field = self.get_by_placeholder(input_form, 'Ex.: John')
            first_name_field.send_keys('  ')
            first_name_field.send_keys(Keys.ENTER)
            new_form = self.get_form(self.browser)

            self.assertIn('Please enter your first name.', new_form.text)

        self.form_field_test_with_callback(callback_first_name)

    def test_empty_last_name_error_test(self):
        def callback_last_name(input_form):
            last_name_field = self.get_by_placeholder(input_form, 'Ex.: Doe')
            last_name_field.send_keys('  ')
            last_name_field.send_keys(Keys.ENTER)
            new_form = self.get_form(self.browser)

            self.assertIn('Please enter your last name.', new_form.text)

        self.form_field_test_with_callback(callback_last_name)

    def test_empty_username_error_test(self):
        def callback_username(input_form):
            username_field = self.get_by_placeholder(input_form, 'Type your username here')
            username_field.send_keys('  ')
            username_field.send_keys(Keys.ENTER)
            new_form = self.get_form(self.browser)

            self.assertIn('This field is required.', new_form.text)

        self.form_field_test_with_callback(callback_username)

    def test_invalid_email_error_test(self):
        def callback_email(input_form):
            email_field = self.get_by_placeholder(input_form, 'Your e-mail address')
            email_field.clear()
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)
            new_form = self.get_form(self.browser)

            self.assertIn('Please enter a valid email address.', new_form.text)

        self.form_field_test_with_callback(callback_email)

    def test_passwords_do_not_match(self):
        def callback_password(input_form):
            password_field = self.get_by_placeholder(input_form, 'Your password here')
            password_field2 = self.get_by_placeholder(input_form, 'Please enter your password again.')
            password_field.clear()
            password_field2.clear()
            password_field.send_keys('P@sswordValid1')
            password_field2.send_keys('P@sswordValid2')
            password_field.send_keys(Keys.ENTER)
            new_form = self.get_form(self.browser)

            self.assertIn('Passwords do not match', new_form.text)

        self.form_field_test_with_callback(callback_password)

