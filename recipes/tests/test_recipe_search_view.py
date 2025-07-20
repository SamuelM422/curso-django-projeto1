from django.urls import reverse
from .test_recipe_base import RecipeTestBase

# Create your tests here.
class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search') + '?q=++')
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<test>'
        response = self.client.get(url)
        self.assertIn('<title>Search results for: &quot;&lt;test&gt;&quot;</title>',
                      response.content.decode('utf-8'))

    def test_recipe_search_can_find_recipe_by_title(self):
        recipe = self.make_recipe(title='Recipe with search term', description='This is the description')
        url = reverse('recipes:search') + '?q=search'
        response = self.client.get(url)
        self.assertIn(recipe.description, response.content.decode('utf-8'))