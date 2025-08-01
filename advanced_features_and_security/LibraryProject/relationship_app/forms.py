from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

Form for user registration
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
