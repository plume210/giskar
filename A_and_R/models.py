from calendar import calendar
from django.db import models
from User.models import User

class Calendar(models.Model):
    user = models.ForeignKey(User, related_name='calendars', on_delete=models.CASCADE)

class Availabilities(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='availabilities')

    def __str__(self):
        return str(self.start) + " " + str(self.end)

    def reduce_availability(self, starts, ends, calendar):
        if self.start < starts and self.end > ends:
            new_avalaibility = Availabilities(start=ends, end=self.end, calendar=calendar)
            self.end = starts
            new_avalaibility.save()
            self.save()
        elif self.start < starts :
            self.end = starts
            self.save()
        elif self.end > ends:
            self.start = ends   
            self.save()
        else:
            self.delete()
class Reservation(models.Model):
    email=models.EmailField()
    title=models.TextField(max_length=200)
    start=models.DateTimeField()
    end=models.DateTimeField()
    calendar = models.ManyToManyField(Calendar)  

