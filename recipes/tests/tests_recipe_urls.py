from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views

# Create your tests here.
class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        home_url = reverse('recipes:home')
        self.assertEqual(home_url, '/')

    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_detail_url_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'recipe_id': 1})
        self.assertEqual(url, '/recipes/1/')

    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')

    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_template_is_correct(self):
        response = self.client.get(reverse('recipes:search') + '?q=test')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')