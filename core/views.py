import datetime

from django.shortcuts import render, redirect
from datetime import date, datetime
from core.models import Location, Attendance


def index(request):
    return render(request, template_name='pages/index.html')


def render_user_dashboard(request):
    return render(request, template_name="pages/user/dashboard.html")


def render_clocking(request):
    if request.method == "POST":
        pass
    clock_type = request.GET.get("type")
    return render(request, template_name='pages/user/clock-action.html', context={'clock': clock_type})


def render_admin_dashboard(request):
    if request.method == "POST":
        pass
    return render(request, template_name='pages/admin/home.html')


def create_location(req):
    return render('')
def view_locations(request):
    if request.method == "POST":
        pass
    return render(request, template_name='pages/admin/locations.html')


def view_employees(request):
    if request.method == "POST":
        pass
    return render(request, template_name='pages/admin/employees.html')



# attendance
def view_attendances(request):
    if request.method == "POST":
        pass
    return render(request, template_name='pages/admin/attendances.html')

def register_attendance(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'POST':
        location = Location.objects.get(code=request.POST.get("code"))
        employee = request.user
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("latitude")
        clock_out_time = datetime.now().time()

        attendance = Attendance.objects.get(employee=employee, date=date.today())
        if attendance is not None: # meaning the user has clocked in already
            attendance.clock_out_time = clock_out_time
            attendance.save()
            # send clock out success message

        # check if all values are valid first
        attendance = Attendance.objects.create(
            location=location,
            employee=employee,
            latitude=latitude,
            longitude=longitude,
            # clocked in time is filled automatically
            clock_out_time=clock_out_time
        )
        attendance.save()
        # check that location matches geolocation of location with the current code
    return render(request, template_name='pages/user/clock-action.html')

