from django import forms
from django.core.exceptions import ValidationError
from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number
from collections import defaultdict

class AuthorRecipeValidator:
    def __init__(self, data, errors=None, error_class=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.errorClass = ValidationError if error_class is None else error_class
        self.data = data
        self.clean()

    def clean(self):
        self.clean_title()
        self.clean_preparation_time()

        cd = self.data
        title = cd.get('title')
        description = cd.get('description')

        if title == description:
            self.errors['title'].append('Cannot be equal do description')
            self.errors['description'].append('Cannot be equal do title')

        if self.errors:
            raise self.errorClass(self.errors)

    def clean_title(self):
        field_value = self.data.get('title')

        if len(field_value) < 5:
            self.errors['title'].append('Title must be at least 5 characters long.')

        return field_value

    def clean_preparation_time(self):
        field_value = self.data.get('preparation_time')

        if not is_positive_number(field_value):
            self.errors['preparation_time'].append('Please, write a positive number')

        return field_value