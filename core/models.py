from django.db import models
from datetime import datetime
from users.models import CustomUser
import uuid


ATTENDANCE_TYPE = (('CI', 'Clocked In'), ('CO', 'Clocked Out'))


class Location(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    code = models.CharField(max_length=128, unique=True, editable=False)
    latitude = models.DecimalField(max_digits=8, decimal_places=4, blank=False, null=False)
    longitude = models.DecimalField(max_digits=8, decimal_places=4, blank=False, null=False)
    radius = models.IntegerField(default=50, blank=False, null=False)
    qr_code_url = models.TextField(max_length=1024, blank=False, null=False)
    

class Attendance(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True, null=False)
    type = models.CharField(max_length=2, choices=ATTENDANCE_TYPE, blank=False, null=False)
