from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ValidationError
from matplotlib.style import available

from A_and_R.models import Availabilities, Calendar, Reservation
from .forms import LoginForm,CreateUser
from .models import User
from django.contrib.auth import authenticate, views
# Create your views here.
class loginView(views.LoginView):
    URL='/login/'
    next_page = '/'
    template_name = 'forms/login.html'

class logoutView(views.LogoutView):
    URL='/logout/'
    next_page = '/'
    template_name = 'forms/logout.html'

def create_user(request):
    form = CreateUser()
    try :
        if request.method == 'POST':
            form = CreateUser(request.POST)
            if form.is_valid():
                user = User()
                user.email = form.cleaned_data['email']
                user.username = form.cleaned_data['username']
                user.set_password(form.cleaned_data['password'])
                user.save()
                cal = Calendar()
                cal.user = user
                cal.save()
                return HttpResponseRedirect('/login/')
        return render(request, 'forms/create_user.html', {'form': form})
    except ValidationError as e:
        return render(request, 'forms/create_user.html', {'form': form, 'error': e})