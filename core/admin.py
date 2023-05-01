from django.contrib import admin
from core.models import Location, Attendance, LeaveRequest

admin.site.register(Location)
admin.site.register(Attendance)
admin.site.register(LeaveRequest)
