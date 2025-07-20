from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from recipes.models import Recipe

# Create your tests here.
class RecipeViewsTest(RecipeTestBase):
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

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))

        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        Recipe.objects.filter(pk=1).delete()
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(title='Recipe not published', is_published=False)
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': recipe.category.id}))

        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'recipe_id': 1}))

        self.assertIs(view.func, views.recipes)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        Recipe.objects.filter(pk=1).delete()
        response = self.client.get(reverse('recipes:recipe', kwargs={'recipe_id': 1}))

        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_dont_loads_recipes_not_published(self):
        recipe = self.make_recipe({'name': 'This is a detail page - It loads one recipe'},
                                  is_published=False)
        response = self.client.get(reverse('recipes:recipe', kwargs={'recipe_id': recipe.id}))

        self.assertEqual(response.status_code, 404)
