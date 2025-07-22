from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import strong_password


class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type your username here'}),
                               error_messages={'required': 'This field is required.',
                                                'unique': 'A user with that username already exists.',
                                               'min_length': 'Ensure this value has at least 4 characters.',
                                               'max_length': 'Ensure this value has at most 65 characters.'},
                                label='Username',
                               min_length=4,
                               max_length=65)
    first_name = forms.CharField(error_messages={'required': 'Please enter your first name.'},
                                 widget=forms.TextInput(attrs={'placeholder': 'Ex.: John'}),
                                 label='First Name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ex.: Doe'}),
                                error_messages={'required': 'Please enter your last name.'},
                                label='Last Name')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your e-mail address'}),
                             error_messages={'required': 'Please enter your email address.'},
                             label='Email',
                             help_text='Required. Inform a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password here'}),
                               error_messages={'required': 'Please enter your password.'},
                               help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                               validators=[strong_password],
                               label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Please enter your password again.'}),
                                error_messages={'required': 'Please enter your password again.'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        # exclude = ['first_name']

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError('This email address is already in use.',
                                  code='invalid')

        return email

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