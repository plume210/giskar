from datetime import datetime,timedelta
from calendar import HTMLCalendar
from .models import Avalaibilities

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()
    
    def formatmonth(self, withyear=True):
        all_object = Avalaibilities.objects.all()
        events = []
        for object in all_object:
            if object.start.year == self.year and object.start.month == self.month:
                events.append(object)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
                cal += f'{self.formatweek(week, events)}\n'
        return cal

    def formatday(self, day, events):
        events_per_day = []
        for event in events:
            if event.start.day <= day and event.end.day >= day:
                events_per_day.append(event)
        d = ''
        for i in range(len(events_per_day)):
            s_hour = events_per_day[i].start.hour
            s_minutes = events_per_day[i].start.minute
            if (day != events_per_day[0].start.day):
                s_hour = "00"
                s_minutes = "00"
            e_hour = events_per_day[i].end.hour
            e_minutes = events_per_day[i].end.minute
            if (day != events_per_day[0].end.day):
                e_hour = "23"
                e_minutes = "59"
            d += f'<div class="event">Available between {s_hour}:{s_minutes} and {e_hour}:{e_minutes}</div>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr 
    def formatweek(self, theweek, events):
        week = ''
        for day, weekday in theweek:
            week += self.formatday(day, events)
        return f'<tr> {week} </tr>'