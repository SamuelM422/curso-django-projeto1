from django.urls import reverse, resolve
import recipes.views.class_based_views as cl
from .test_recipe_base import RecipeMixIn
from recipes.models import Recipe

# Create your tests here.
class RecipeDetailViewTest(RecipeMixIn):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))

        self.assertIs(view.func.view_class, cl.RecipeDetailView) # type: ignore

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        Recipe.objects.filter(pk=1).delete()
        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_dont_loads_recipes_not_published(self):
        recipe = self.make_recipe({'name': 'This is a detail page - It loads one recipe'},
                                  is_published=False)
        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': recipe.id}))

        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_returns_correct_recipe_data(self):
        recipe = self.make_recipe({'name': 'This is a detail page - It loads one recipe'})
        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': recipe.id}))
        content = response.content.decode('utf-8')

        self.assertIn('This is a detail page - It loads one recipe', content)