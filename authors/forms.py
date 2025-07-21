from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name)
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()

def set_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_placeholder(self.fields['first_name'], 'Type your first name here')
        set_placeholder(self.fields['email'], 'Your e-mail address')
        set_placeholder(self.fields['username'], 'Ex.: John')
        set_placeholder(self.fields['last_name'], 'Ex.: Doe')

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password here'}),
                               error_messages={'required': 'Please enter your password.'},
                               help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Type your password again here'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        # exclude = ['first_name']

        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }

        help_texts = {
            'email': 'Required. Inform a valid email address.',
        }

        error_messages = {
            'username': {
                'required': 'This field is required.',
                'unique': 'A user with that username already exists.',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Type your first name here'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Type your password here'}),
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'password2' in self.cleaned_data:
            raise ValidationError(
                '"password2" is in your password',
                code='invalid'
            )

        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError(
                {'password': 'Passwords do not match',
                 'password2': 'Passwords do not match'},
                code='invalid'
            )

        return cleaned_data