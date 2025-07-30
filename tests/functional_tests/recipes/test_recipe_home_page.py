import time
from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest.mock import patch
import pytest

@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('No recipes found', body.text)

    def test_recipe_search_input_can_find_correct_recipes(self):
        # Creating recipes
        recipes = self.make_recipes(10)

        # Setting the search term
        recipes[0].title = 'Title searched'
        recipes[0].save()

        # User opening the browser and selecting the search bar
        self.browser.get(self.live_server_url)

        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search recipes here"]'
        )

        # User searching the title of the recipe
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        time.sleep(5)

        # Assertion
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn(recipes[0].title, body.text)

    @patch('recipes.views.base.PER_PAGE', 2)
    def test_recipe_home_page_pagination(self):
        # Creating recipes
        self.make_recipes(10)

        # User opening the browser
        self.browser.get(self.live_server_url)

        # User sees the navigation and clicks on page 2
        page2 = self.browser.find_element(By.XPATH,
                                          '//a[@aria-label="go to page 2"]')

        page2.click()

        # User sees that navigation page 2 has two recipes
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )