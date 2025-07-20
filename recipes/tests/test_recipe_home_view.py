from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from recipes.models import Recipe

# Create your tests here.
class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_views_functions_is_correct(self):
        view = resolve(reverse('recipes:home'))

        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        Recipe.objects.filter(pk=1).delete()
        response = self.client.get(reverse('recipes:home'))

        self.assertIn('<h1>No recipes found</h1>', response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        recipe = self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        context = response.context['recipes']
        content = response.content.decode('utf-8')

        self.assertEqual(len(context), 1)
        self.assertIn(recipe.title, content)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(title='Recipe not published', is_published=False)
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        self.assertNotIn(recipe.title, content)