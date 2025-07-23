from tests.functional_tests.authors.base import AuthorsBaseTest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
import pytest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        user = User.objects.create_user(
            username='my_user',
            password='my_password'
        )

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(
            By.CLASS_NAME,
            'main-form'
        )
        username_field = self.get_by_placeholder(form, 'Type your username here')
        password_field = self.get_by_placeholder(form, 'Your password here')

        username_field.send_keys(user.username)
        password_field.send_keys('my_password')

        form.submit()

        self.assertIn(
            'You are logged in with my_user.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))

        self.assertIn('Not Found', self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_form_login_is_invalid(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username_field = self.get_by_placeholder(form, 'Type your username here')
        password_field = self.get_by_placeholder(form, 'Your password here')

        username_field.send_keys(' ')
        password_field.send_keys(' ')

        form.submit()

        self.assertIn(
            'Invalid username or password.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_with_invalid_credentials(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username_field = self.get_by_placeholder(form, 'Type your username here')
        password_field = self.get_by_placeholder(form, 'Your password here')

        username_field.send_keys('invalid_username')
        password_field.send_keys('invalid_password')

        form.submit()

        self.assertIn(
            'Invalid credentials.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )