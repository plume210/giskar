from django.forms import ValidationError
from django.shortcuts import render
import pytz
from .forms import AvailabilitiesForm, ReservationsForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.views import generic
from .utils import *
from django.utils.safestring import mark_safe
from datetime import date, datetime
utc = pytz.UTC

def home(request):
    return render(request, 'calendars/index.html')

class CalendarView(generic.TemplateView):
    model = Reservation
    template_name = 'calendars/calendar.html'
    def get_context_data(self, date=date.today() ,**kwargs):
        context = super().get_context_data(**kwargs)
        try :
            year = int(context['year'][:-1])
        except:
            year = date.today().year
        try :
            month = int(context['month'][:-1])
        except:
            if (year == date.today().year):
                month = date.today().month
            else:
                month = 1
        # use today's date for the calendar
        # Instantiate our calendar class with today's year and date
        cal = Calendar(year,month)
        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['left_button'] = mark_safe(self.create_button_left(year, month))
        context['right_button'] = mark_safe(self.create_right_button(year, month))
        context['calendar'] = mark_safe(html_cal)
        return context
    
    def create_button_left(self, year, month):
        year_before = year
        month_before = month - 1
        if (month == 1):
            year_before = year - 1
            month_before = 12        
        return "<form action=/" + str(year_before) + "/" + str(month_before) + "/>  <button class=\"date-button\"><</button></form>"
    def create_right_button(self, year, month):
        year_after = year
        month_after = month + 1
        if (month == 12):
            year_after = year + 1
            month_after = 1
        return "<form action=/" + str(year_after) + "/" + str(month_after) + "/>  <button class=\"date-button\">></button></form>"
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

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
                available.reduce_avalaibility(reservation.start, reservation.end)
                return HttpResponseRedirect('/')
        return render(request, 'calendars/create.html', {'form': form})
    except ValidationError as e:
        return HttpResponse(e)
    
def delete_reservation(request):
    pass

# Create my availability here.
def create_avalaibility(request):   
    form = AvailabilitiesForm()
    if request.method == 'POST':
        form = AvailabilitiesForm(request.POST)
        if form.validate():
            availability = Avalaibilities(start = datetime.combine(form.cleaned_data['start'], form.cleaned_data['start_hour']),
                             end = datetime.combine(form.cleaned_data['end'], form.cleaned_data['end_hour']))
            availability.save()
            Reservation.objects.filter(start__range=(availability.start, availability.end)).delete()
            return HttpResponseRedirect('/')
    list_availability(request)
    return render(request, 'calendars/create.html', {'form': form})

def list_availability(request):
    availabilities = Avalaibilities.objects.values_list()
    event = []
    for availability in availabilities:
        event.append({'title':"Available", 'start':availability[1].strftime("%Y-%m-%dT%H:%M:%S"), 'end':availability[2].strftime("%Y-%m-%dT%H:%M:%S")})
    print(event)
    return render(request, 'calendars/index.html', {'event': event})