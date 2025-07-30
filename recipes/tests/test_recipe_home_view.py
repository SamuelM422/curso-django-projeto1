from django.urls import reverse, resolve
import recipes.views.class_based_views as class_based_views
from .test_recipe_base import RecipeMixIn
from recipes.models import Recipe
from unittest.mock import patch

# Create your tests here.
class RecipeHomeViewTest(RecipeMixIn):
    def test_recipe_home_views_functions_is_correct(self):
        view = resolve(reverse('recipes:home'))

        self.assertIs(view.func.view_class, class_based_views.RecipeListViewHome) # type: ignore

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        Recipe.objects.filter(pk=1).delete()
        response = self.client.get(reverse('recipes:home'))

        self.assertIn('No recipes found', response.content.decode('utf-8'))

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

    def test_recipe_home_is_paginated(self):
        for i in range(8):
            kwargs = {
                'slug': f'r{i}',
                'author_data': {
                    'username': f'author{i}'
                }
            }
            self.make_recipe(**kwargs)

        with patch('recipes.views.base.PER_PAGE', 3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)