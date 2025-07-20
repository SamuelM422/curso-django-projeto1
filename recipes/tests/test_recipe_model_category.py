from django.core.exceptions import ValidationError
from .test_recipe_base import RecipeTestBase

class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self):
        self.category = self.make_category()

        return super().setUp()

    def test_category_name_representation(self):
        self.category.name = 'Category Name'
        self.category.full_clean()
        self.category.save()
        self.assertEqual(str(self.category), self.category.name)

    def test_category_name_raises_error_if_name_has_more_than_65_chars(self):
        self.category.name = 'A' * 70
        with self.assertRaises(ValidationError):
            self.category.full_clean()
