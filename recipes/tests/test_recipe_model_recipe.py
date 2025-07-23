from .test_recipe_base import RecipeMixIn, Recipe
from django.core.exceptions import ValidationError

class RecipeModelTest(RecipeMixIn):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_not_default(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='test_default_author'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug-not-default',
            preparation_time=10,
            preparation_time_unit='Minutes',
            servings=5,
            servings_unit='Portions',
            preparation_steps='Recipe Preparation Steps',
            cover='recipes/dummyImage.png'
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        self.recipe.title = 'A' * 70

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_fields_max_length(self):
        fields = [
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ]

        for field, max_length in fields:
            with self.subTest(field=field, max_length=max_length):
                setattr(self.recipe, field, 'A' * (max_length + 1))
                with self.assertRaises(ValidationError):
                    self.recipe.full_clean()

    def test_recipe_preparation_is_html_false_by_default(self):
        recipe = self.make_recipe_not_default()
        self.assertFalse(recipe.preparation_steps_is_html)

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_not_default()
        self.assertFalse(recipe.is_published)

    def test_recipe_string_representation(self):
        self.recipe.title = 'Recipe Title'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), self.recipe.title)