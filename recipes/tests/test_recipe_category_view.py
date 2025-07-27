from django.urls import reverse, resolve
import recipes.views.class_based_views as class_based_views
from .test_recipe_base import RecipeMixIn
from recipes.models import Recipe

# Create your tests here.
class RecipeCategoryViewTest(RecipeMixIn):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))

        self.assertIs(view.func.view_class, class_based_views.RecipeListViewCategory) # type: ignore

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        Recipe.objects.filter(pk=1).delete()
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(title='Recipe not published', is_published=False)
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': recipe.category.id}))

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_returns_correct_recipe_data(self):
        recipe = self.make_recipe(title='This is a category page - It loads one recipe')
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': recipe.category.id}))
        content = response.content.decode('utf-8')

        self.assertIn('This is a category page - It loads one recipe', content)