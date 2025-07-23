from django.test import TestCase
from recipes.models import Recipe, User, Category


class RecipeMixIn(TestCase):
    @staticmethod
    def make_category(name='Category'):
        return Category.objects.create(name=name)

    @staticmethod
    def make_author(
                    first_name='John',
                    last_name='Doe',
                    username='johndoe',
                    password='123456',
                    email='johndoe@email.com',
                    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(self,
                    category_data=None,
                    author_data=None,
                    title='Recipe Title',
                    description='Recipe Description',
                    slug='recipe-slug',
                    preparation_time=10,
                    preparation_time_unit='Minutes',
                    servings=5,
                    servings_unit='Portions',
                    preparation_steps='Recipe Preparation Steps',
                    preparation_steps_is_html=False,
                    is_published=True,
                    cover='recipes/dummyImage.png'
                    ):

        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            cover=cover
        )

    def make_recipes(self, qty=10):
        recipes = []
        for i in range(qty):
            kwargs = {'slug': f'recipe-slug-{i}',
                      'title': f'Recipe Title {i}',
                      'author_data': {'username': f'author-{i}'}}
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes