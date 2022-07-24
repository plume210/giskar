from django.contrib import admin

from A_and_R.models import Availabilities, Reservation

# Register your models here.
admin.site.register(Availabilities)
admin.site.register(Reservation)