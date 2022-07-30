from calendar import calendar
from tracemalloc import start
from django.forms import ValidationError
from django.shortcuts import render
from matplotlib.style import available
import pytz
from requests import get
from .forms import AvailabilitiesForm, ReservationsForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib import messages
from datetime import date, datetime, timedelta, time
utc = pytz.UTC

def home(request, error):
    return render(request, 'index.html', error)

# Create my reservation here.
# if you reserve a slot that is not available, there will be an error.
def create_reservation(request, email="", date_start=str(date.today().strftime('%a %b %d %Y %H:%M:%S')),date_end=str(date.today().strftime('%a %b %d %Y %H:%M:%S'))):
    initial_begin_date = datetime.strptime(date_start, '%a %b %d %Y %H:%M:%S')
    initial_end_date = datetime.strptime(date_end, '%a %b %d %Y %H:%M:%S')
    initial_hours_begin  = initial_begin_date.time() 
    initial_hours_end = initial_end_date.time()
    owner_email = ""
    if (request.user.is_authenticated):
        owner_email = request.user.email
    form = ReservationsForm(initial={'start': initial_begin_date, 'end': initial_end_date,'email': owner_email, 'start_hour': initial_hours_begin, 'end_hour': initial_hours_end})
    try :
        if request.method == 'POST':
            form = ReservationsForm(request.POST)
            available = form.validate()
            reservation = Reservation()
            reservation.title = form.cleaned_data['title']
            reservation.start = datetime.combine(form.cleaned_data['start'], form.cleaned_data['start_hour'])
            reservation.end = datetime.combine(form.cleaned_data['end'], form.cleaned_data['end_hour'])
            reservation.end = utc.localize(reservation.end)
            reservation.start = utc.localize(reservation.start)
            reservation.email = form.cleaned_data['email']
            reservation.save()
            reservation.calendar.add(Calendar.objects.get(user=User.objects.get(email=email)))
            available.reduce_availability(reservation.start, reservation.end, reservation.calendar)
            if (request.user.is_authenticated):
                reservation.calendar.add(Calendar.objects.get(user=request.user))
                owner_availability = Availabilities.objects.get(start__lte = reservation.start, end__gte = reservation.end , calendar=Calendar.objects.get(user=User.objects.get(email=request.user.email)))
                owner_availability.reduce_availability(reservation.start, reservation.end, owner_availability.calendar)
            return HttpResponseRedirect('/')
        return render(request, 'forms/create_reservation.html', {'form': form})
    except ValidationError as e:
        return render(request=request, template_name='forms/create_reservation.html', context={'form': form, 'error': e})
    
def delete_reservation(request, email, date_start, date_end):
    try:
        if request.method == 'GET':
            initial_begin_date = datetime.strptime(date_start, '%a %b %d %Y %H:%M:%S')
            initial_end_date = datetime.strptime(date_end, '%a %b %d %Y %H:%M:%S')
            reservation = Reservation.objects.get(email=email, start=initial_begin_date, end=initial_end_date, calendar=Calendar.objects.get(user=request.user))
            for var in reservation.calendar.all():
                if var.user == request.user:   # only the user can delete his reservation
                    reservation.delete()
            return HttpResponseRedirect('/')
    except :
        return get_calendar_detail(request, "You should ask the owner to delete your reservation")

# Create my availability here.
def create_availabilities(request):   
    form = AvailabilitiesForm()
    if not request.user.is_authenticated:
        return render(request, 'index.html', {'error': "You must be logged in to create an availability"})
    try :
        if request.method == 'POST':
            form = AvailabilitiesForm(request.POST)
            if form.validate():
                # Combine date and hours
                start_time = datetime.combine(form.cleaned_data['start'], form.cleaned_data['start_hour'])
                end_time = datetime.combine(form.cleaned_data['end'], form.cleaned_data['end_hour'])
                # Available only between 9 and 20h every day, i am a busy man
                while (start_time < end_time): 
                    availability = Availabilities()
                    availability.start = start_time
                    if (start_time.day == end_time.day and start_time.month == end_time.month and start_time.year == end_time.year):
                        availability.end = end_time
                    else :
                        availability.end =  start_time.replace(hour=20, minute=0, second=0, microsecond=0)
                    start_time = start_time + timedelta(days=1)
                    start_time = start_time.replace(hour=9, minute=0, second=0)
                    availability.calendar = Calendar.objects.get(user=request.user)
                    availability.save()
                return HttpResponseRedirect('/')
        return render(request, 'forms/create_availabilities.html', {'form': form})
    except ValidationError as e:
        return render(request=request, template_name='forms/create_availabilities.html', context={'form': form, 'error': e})

def get_calendars_by_searching(request, name):
    owner_email = ""
    owner = ""
    if request.user.is_authenticated:
        owner_email = request.user.email
        owner = request.user.username
    if (not User.objects.filter(username=name).exists()):
        return render(request, 'index.html', {'error': "User not found"})
    email = User.objects.get(username=name).email
    calendars = Calendar.objects.get(user=User.objects.get(username=name))
    available = Availabilities.objects.filter(calendar=calendars).values()
    availability_list = []
    for availability in available:
        availability_list.append({'title':"Available", 'start':availability["start"].strftime("%Y-%m-%dT%H:%M:%S"), 'end':availability["end"].strftime("%Y-%m-%dT%H:%M:%S")})
    return render(request, 'index.html', {'availabilities': availability_list, "calendar_name": email, 'owner': owner, 'email': owner_email})

def get_calendar_detail(request, error=""):
    availabilities = []
    reservations = []
    name = ""
    email = ""
    if (request.user.is_authenticated == True):
        name = request.user.username
        email = request.user.email
        if (Availabilities.objects.filter(calendar=Calendar.objects.get(user=request.user)).exists()):
            availabilities = Availabilities.objects.filter(calendar=Calendar.objects.get(user=request.user)).values()    # get all availabilities
        if (Reservation.objects.filter(calendar=Calendar.objects.get(user=request.user)).exists()):
            reservations = Reservation.objects.filter(calendar=Calendar.objects.get(user=request.user)).values()
    availability_list = []
    reservation_list = []
    for availability in availabilities:
        availability_list.append({'title':"Available", 'start':availability["start"].strftime("%Y-%m-%dT%H:%M:%S"), 'end':availability["end"].strftime("%Y-%m-%dT%H:%M:%S")})
    for reservation in reservations:
        reservation_list.append({'title': reservation["title"], 'start':reservation["start"].strftime("%Y-%m-%dT%H:%M:%S"), 'end':reservation["end"].strftime("%Y-%m-%dT%H:%M:%S"), 'email': reservation["email"]})
    return render(request, 'index.html', {'availabilities': availability_list, 'reservations': reservation_list, 'owner': name, 'email': email , "error":error}) #a changer
