from django.forms import ModelForm, ValidationError
from .models import *

class CreateUser(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
