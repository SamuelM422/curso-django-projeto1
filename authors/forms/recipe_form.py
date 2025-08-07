from django import forms
from django.core.exceptions import ValidationError
from recipes.models import Recipe
from utils.django_forms import add_attr
from authors.validators import AuthorRecipeValidator
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
        AuthorRecipeValidator(cleaned_data)

        return cleaned_data