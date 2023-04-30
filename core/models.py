from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
import uuid


ATTENDANCE_TYPE = (('CI', 'Clocked In'), ('CO', 'Clocked Out'))


class Location(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    code = models.CharField(default=uuid.uuid4(), editable=False)
    latitude = models.DecimalField(decimal_places=10, blank=False, null=False)
    longitude = models.DecimalField(decimal_places=10, blank=False, null=False)
    radius = models.IntegerField(default=50, blank=False, null=False)
    qr_code_url = models.TextField(blank=False, null=False)
    

class Attendance(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=datetime.now(), null=False)
    type = models.CharField(choices=ATTENDANCE_TYPE, blank=False, null=False)
