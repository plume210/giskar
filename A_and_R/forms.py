import datetime
from django import forms
from django.core.exceptions import ValidationError
import pytz
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'

utc=pytz.UTC

class AvailabilitiesForm(forms.ModelForm):
    start_hour = forms.TimeField(widget=TimeInput())
    end_hour = forms.TimeField(widget=TimeInput())
    class Meta:
        model = Availabilities
        fields = ['start', 'end']
        widgets = {"start": DateInput(), "end": DateInput()}
    
    def validate(self):
        super().is_valid()
        start_time = self.cleaned_data.get('start')
        end_time = self.cleaned_data.get('end')
        if start_time > end_time:
            raise ValidationError("Start time is after end time")
        return True
    
class ReservationsFormDelete(forms.ModelForm):
    start_hour = forms.TimeField(widget=TimeInput())
    end_hour = forms.TimeField(widget=TimeInput())
    class Meta:
        model = Reservation
        fields = ['start', 'end', 'email']
        widgets = {"start": DateInput(), "end": DateInput()}
    
    def validate(self):
        super().is_valid()
        start = datetime.datetime.combine(self.cleaned_data['start'],self.cleaned_data['start_hour'])
        start = utc.localize(start)
        end = datetime.datetime.combine(self.cleaned_data['end'],self.cleaned_data['end_hour'])
        end = utc.localize(end)
        delete = Reservation.objects.get(start=start, end=end, email=self.cleaned_data['email'])
        return delete

class ReservationsForm(forms.ModelForm):
    start_hour = forms.TimeField(widget=TimeInput())
    end_hour = forms.TimeField(widget=TimeInput())
    class Meta:
        model = Reservation
        fields = ['title', 'email' ,'start', 'end']
        widgets = {"start": DateInput(), "end": DateInput()}
    
    def validate(self):
        super().is_valid()
        start = datetime.datetime.combine(self.cleaned_data['start'],self.cleaned_data['start_hour'])
        start = utc.localize(start)
        end = datetime.datetime.combine(self.cleaned_data['end'],self.cleaned_data['end_hour'])
        end = utc.localize(end)
        all_availabilitys = Availabilities.objects.all()
        available = None
        for availability in all_availabilitys:
            if availability.start < start and availability.end > end:
                available = availability
                break
        if (available == None):
            raise ValidationError("This time is not available")
        if start > end:
            raise ValidationError("Start time is after end time")
        return available