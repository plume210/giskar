from django.db import models

class Availabilities(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return str(self.start) + " " + str(self.end)

    def reduce_availability(self, starts, ends):
        if self.start < starts and self.end > ends:
            new_avalaibility = Availabilities(start=ends, end=self.end)
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