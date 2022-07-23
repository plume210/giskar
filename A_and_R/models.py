from django.db import models
from matplotlib.style import available

class Avalaibilities(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return str(self.start) + " " + str(self.end)

    def reduce_avalaibility(self, starts, ends):
        if self.start < starts and self.end > ends:
            new_avalaibility = Avalaibilities(start=ends, end=self.end)
            self.end = starts
            new_avalaibility.save()
            self.save()
        elif self.start < starts :
            self.end = starts
            self.save()
        elif self.end > ends:
            self.start = ends   
            self.save()

class Reservation(models.Model):
    email=models.EmailField()
    title=models.TextField(max_length=200)
    start=models.DateTimeField()
    end=models.DateTimeField()