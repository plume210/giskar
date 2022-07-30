"""giskar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path
from django.contrib import admin
from A_and_R import views
from User import views as user_views
app_name='A_and_R'
urlpatterns = [
    re_path(r'^admin/', admin.site.urls, name='admin'),
    re_path(r'^$', views.get_calendar_detail, name='home'),
    re_path(r'^delete_reservation/((?P<email>[a-z]*@[a-z]*.[a-z]*)/)?((?P<date_start>[0-z ]*)/)?((?P<date_end>[0-z ]*)/)?$', views.delete_reservation, name='delete_reservation'),
    re_path(r'^create_reservation/((?P<email>[a-z]*@[a-z]*.[a-z]*)/)?((?P<date_start>[0-z ]*)/)?((?P<date_end>[0-z ]*)/)?$', views.create_reservation, name='create_reservation'),
    re_path(r'^create_availabilities/$', views.create_availabilities, name='create_availability'),
    re_path(r'^login/$', user_views.loginView.as_view(), name='login'),
    re_path(r'^register/$', user_views.create_user, name='register'),
    re_path(r'^logout/$', user_views.logoutView.as_view(), name='logout'),
    re_path(r'^(?P<name>[a-z ]*)/$', views.get_calendars_by_searching, name='get_calendars'),
]
