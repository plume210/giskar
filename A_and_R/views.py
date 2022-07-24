import email
from django.forms import ValidationError
from django.shortcuts import render
import pytz
from .forms import AvailabilitiesForm, ReservationsForm, ReservationsFormDelete
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from datetime import datetime, timedelta, time
utc = pytz.UTC

def home(request):
    return render(request, 'calendars/index.html')

# Create my reservation here.
# if you reserve a slot that is not available, there will be an error.
def create_reservation(request):
    form = ReservationsForm()
    try :
        if request.method == 'POST':
            form = ReservationsForm(request.POST)
            available = form.validate()
            if available != None :
                reservation = Reservation()
                reservation.title = form.cleaned_data['title']
                reservation.start = datetime.combine(form.cleaned_data['start'], form.cleaned_data['start_hour'])
                reservation.end = datetime.combine(form.cleaned_data['end'], form.cleaned_data['end_hour'])
                reservation.end = utc.localize(reservation.end)
                reservation.start = utc.localize(reservation.start)
                reservation.email = form.cleaned_data['email']
                reservation.save()
                available.reduce_availability(reservation.start, reservation.end)
                return HttpResponseRedirect('/')
        return render(request, 'calendars/create_reservation.html', {'form': form})
    except ValidationError as e:
        return HttpResponse(e)
    
def delete_reservation(request):
    form = ReservationsFormDelete()
    if request.method == 'POST':
        form = ReservationsFormDelete(request.POST)
        delete = form.validate()
        if (delete != None):
            delete.delete()
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("Error wrong email or date")
    return render(request, 'calendars/delete_reservation.html', {'form': form})

# Create my availability here.
def create_availability(request):   
    form = AvailabilitiesForm()
    if request.method == 'POST':
        form = AvailabilitiesForm(request.POST)
        if form.validate():
            print(form.cleaned_data["start_hour"])
            start_time = datetime.combine(form.cleaned_data['start'], form.cleaned_data['start_hour'])
            end_time = datetime.combine(form.cleaned_data['end'], form.cleaned_data['end_hour'])
            while (start_time < end_time):   
                availability = Availabilities()
                availability.start = start_time
                if (start_time.day == end_time.day):
                    availability.end = end_time
                else :
                    availability.end = datetime.combine(start_time.date(), time(hour=19,minute=59,second=59))   # end of the day
                availability.save()
                start_time = start_time + timedelta(days=1)
                start_time = start_time.replace(hour=9, minute=0, second=0) 
            return HttpResponseRedirect('/')
    return render(request, 'calendars/create.html', {'form': form})

def list_availability(request):
    availabilities = Availabilities.objects.values_list()
    event = []
    for availability in availabilities:
        event.append({'title':"Available", 'start':availability[1].strftime("%Y-%m-%dT%H:%M:%S"), 'end':availability[2].strftime("%Y-%m-%dT%H:%M:%S")})
    return render(request, 'calendars/index.html', {'event': event})