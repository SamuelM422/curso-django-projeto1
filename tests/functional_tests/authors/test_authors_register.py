from tests.functional_tests.authors.base import AuthorsBaseTest
from django.urls import reverse

class AuthorsRegisterTest(AuthorsBaseTest):
    def test_the_test(self):
        self.browser.get(self.live_server_url + reverse('authors:register'))