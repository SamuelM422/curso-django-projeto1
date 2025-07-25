from django import forms
from django.core.exceptions import ValidationError
from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number
from collections import defaultdict

class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._custom_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'preparation_time',
                  'preparation_time_unit', 'servings',
                  'servings_unit', 'preparation_steps',
                  'cover',]

        widgets = {
            'cover': forms.FileInput(
                attrs={'class': 'span-2'}
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Portions', 'Portions'),
                    ('Pieces', 'Pieces'),
                    ('Peoples', 'Peoples')
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Hours', 'Hours'),
                    ('Minutes', 'Minutes'),
                )
            )
        }

    def clean(self):
        cleaned_data = super().clean()

        cd = self.cleaned_data
        title = cd.get('title')
        description = cd.get('description')

        if title == description:
            self._custom_errors['title'].append('Cannot be equal do description')
            self._custom_errors['description'].append('Cannot be equal do title')

        if self._custom_errors:
            raise ValidationError(self._custom_errors)

        return cleaned_data

    def clean_title(self):
        field_value = self.cleaned_data.get('title')

        if len(field_value) < 5:
            self._custom_errors['title'].append('Title must be at least 5 characters long.')

        return field_value

    def clean_preparation_time(self):
        field_value = self.cleaned_data.get('preparation_time')

        if not is_positive_number(field_value):
            self._custom_errors['preparation_time'].append('Please, write a positive number')

        return field_value