from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_webdriver
from recipes.tests.test_recipe_base import RecipeMixIn

class RecipeBaseFunctionalTest(RecipeMixIn, StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()

        self.browser = make_webdriver()

    def tearDown(self):
        super().tearDown()

        self.browser.quit()