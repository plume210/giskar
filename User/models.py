from django.contrib.auth.models import AbstractUser
from A_and_R.models import *
# Create your models here.
class User(AbstractUser):
    reservations_slot = models.OneToOneField(Reservation, blank=True)
    availabilities_slot = models.OneToOneField(Availabilities, blank=True)
    
