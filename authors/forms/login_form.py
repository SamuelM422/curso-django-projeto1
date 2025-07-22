from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type your username here'}),
                               label='Username')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password here'}),
                               label='Password')