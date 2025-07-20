from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from recipes.models import Recipe

# Create your tests here.
class RecipeDetailViewTest(RecipeTestBase):
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