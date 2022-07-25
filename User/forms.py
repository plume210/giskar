from django.forms import ModelForm
from .models import *

class CreateUser(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']