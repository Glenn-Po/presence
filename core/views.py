from django.http import JsonResponse, HttpResponseRedirect, QueryDict
from django.db.models import Count, Q
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from users.models import CustomUser, Profile
from users.forms import ProfileForm
from core.models import Location, Attendance, LeaveRequest
from core.forms import AttendanceForm, EmployeeForm, LocationForm
from core.decorators import authorize_manager_only
from datetime import date, datetime
from uuid import uuid4
from .utils import delete_image_from_cloudinary, position_within_area, text_to_qr_code_data_uri, upload_data_uri_to_cloudinary


'''
Non-interactive parts
1. The index page
'''


def index(request):
    return render(request, template_name='pages/index.html')


'''
Admin Dashboard
'''

'''
Admin Dashboard - Home
-Display numbers & display requests
-delete a leave request
'''


@login_required(login_url='/account/login')
@authorize_manager_only(redirect_url='/employee/dashboard')
@require_GET
def render_admin_dashboard(request):
    employee_count = CustomUser.objects.select_related('profile').count()
    location_count = Location.objects.count()
    present_today_count = Attendance.objects.filter(
        date=datetime.today()).count()

    leave_requests = LeaveRequest.objects.all()

    context = {
        'employee_count': employee_count,
        'location_count': location_count,
        'present_today_count': present_today_count,
        'leave_requests': leave_requests,
    }
    return render(request, template_name='pages/admin/home.html', context=context)


@authorize_manager_only(redirect_url='/employee/dashboard')
@login_required(login_url='/account/login')
def delete_leave_request(request, id):
    get_object_or_404(LeaveRequest, pk=id).delete()
    return HttpResponseRedirect('/manager/dashboard')


'''
Admin Dashboard - Attendances
-Display attendances
-Filter attendance by employee and by date
-view employee attendances on callendar
'''


@login_required(login_url='/account/login')
@require_GET
@authorize_manager_only(redirect_url='/employee/dashboard')
def view_attendance(request):
    attendances = Attendance.objects.all()
    return render(request, template_name='pages/admin/attendances.html', context={"attendances": attendances})


def filter_attendance_by_date(request, date):
    return


def filter_attendance_by_employee(request, id):
    return


'''
Admin Dashboard - Locations
-main dashboard displaying locations
-create location
-update location
-delete location
'''


@login_required(login_url='/account/login')
@require_GET
@authorize_manager_only(redirect_url='/employee/dashboard')
def view_locations(request):
    locations = Location.objects.annotate(attendance_count=Count(
        "attendance", filter=Q(attendance__date=datetime.today())))
    context = {"locations": locations}
    return render(request, template_name='pages/admin/locations.html', context=context)


@login_required(login_url='/account/login')
@authorize_manager_only(redirect_url='/employee/dashboard')
def create_location(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # iterate to initially clear the message queue
    if request.method == "POST":
        form = LocationForm(request.POST, )
        if form.is_valid():
            name = form.cleaned_data["name"]
            longitude = form.cleaned_data["longitude"]
            latitude = form.cleaned_data["latitude"]
            radius = form.cleaned_data["radius"]

            print(radius, latitude, longitude)
            # generate qr code and store in cloud
            code = uuid4()
            qr_code_data = text_to_qr_code_data_uri(code)
            download_url = upload_data_uri_to_cloudinary(qr_code_data)

            print("Uploaded: "+download_url)
            location = Location(name=name, code=code, latitude=latitude,
                                longitude=longitude, radius=radius, qr_code_url=download_url)
            location.save()
            messages.success(request,
                             f"You have succcessully create location <<{name}>>", extra_tags="success")
        else:
            messages.error(request,
                           f"You request failed. Check that correct values were entered", extra_tags="error")

    return render(request, template_name='pages/admin/create/location.html')


def update_location(request, id):
    location = get_object_or_404(Location, pk=id)
    response = {
        'success': False,
    }
    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            response["success"] = True
    context = {"response": response, "location": "Location"}
    return render(request, template_name='pages/admin/update/location.html', context=context)


@login_required(login_url='/account/login')
@authorize_manager_only(redirect_url='/employee/dashboard')
def delete_location(request, id):
    location = get_object_or_404(Location, pk=id)
    delete_image_from_cloudinary(location.qr_code_url)
    location.delete()
    return HttpResponseRedirect('/manager/dashboard/locations')


'''
Admin Dashboard - Employees
-main dashboard displaying employees
-create employee user account
-update user account
-delete account
'''


@login_required(login_url='/account/login')
@authorize_manager_only(redirect_url='/employee/dashboard')
def view_employees(request):
    employees = CustomUser.objects.all()
    return render(request, template_name='pages/admin/employees.html', context={"employees": employees})


@login_required(login_url='/account/login')
@authorize_manager_only(redirect_url='/employee/dashboard')
def view_employee(request, id):
    employee = CustomUser.objects.filter(pk=id).first()
    print(employee)
    return
    # return render(request, template_name='pages/admin/employees.html', context={"employee": employee})


@login_required(login_url='/account/login')
@authorize_manager_only(redirect_url='/employee/dashboard')
def create_employee(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # iterate to initially clear the message queue
    form = EmployeeForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            print(form.cleaned_data)
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            cpassword = form.cleaned_data["cpassword"]

            name = form.cleaned_data["name"]
            dob = form.cleaned_data["dob"]
            role = form.cleaned_data["role"]
            start_date = form.cleaned_data["start_date"]
            address = form.cleaned_data["address"]
            telephone = form.cleaned_data["telephone"]
            is_manager = form.cleaned_data["is_manager"]

            if cpassword == password:
                try:
                    user = CustomUser.objects.create_user(
                        email=email, password=password)
                    profile = Profile(user=user, name=name, date_of_birth=dob,
                                      role=role, start_date=start_date, telephone=telephone,
                                      address=address, is_manager=is_manager)
                    profile.save()
                    messages.success(
                        request, f"Employee's account <<{name}>> has been created", extra_tags='success')
                except IntegrityError:
                    messages.error(
                        request, f"There is already a user with this email.", extra_tags='error')
            else:
                messages.error(
                    request, f"Passwords did not match", extra_tags='error')
        else:
            messages.error(
                request, f"Your form contained some errors", extra_tags='error')
    print(form.errors)
    return render(request, template_name='pages/admin/create/employee.html', context={'form': form})


def update_employee(request, id):
    success = False
    employee = get_object_or_404(CustomUser, pk=id)
    profile = employee.profile
    form = ProfileForm(request.POST, profile)
    if form.is_valid():
        form.save()
        success = True
    return render(request, template_name='pages/admin/update/employee.html', context={'success': success})


@login_required(login_url='/account/login')
@authorize_manager_only(redirect_url='/employee/dashboard')
def delete_employee(request, id):
    get_object_or_404(CustomUser, pk=id).delete()
    return HttpResponseRedirect('/manager/dashboard/employees')


'''
User dashboard views and actions:

1. Deciding to put clock in or clockout on dash page. or nothing clocking if all are fulfilled
2. registering the attendance. ie doing the clocking
'''


@login_required(login_url='/account/login')
def render_user_dashboard(request):
    attendance = Attendance.objects.filter(
        employee=request.user.id, date=date.today()).first()
    # states: NONE, IN_ONLY, BOTH
    # cloked in only: True, clocked in but not out: false, clocked in and out: None
    print(attendance)
    clocked_in_state = 'NONE' if attendance is None else (
        'IN_ONLY' if attendance.clock_out_time is None else 'BOTH')
    print(clocked_in_state)
    context = {
        "clocked_in_state": clocked_in_state, "attendance": attendance}
    return render(request, template_name="pages/user/dashboard.html", context=context)


@login_required(login_url='/account/login')
def request_leave(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # iterate to initially clear the message queue

    if request.method == 'POST':
        try:
            days_off = int(request.POST.get("days_off"))
            start_date = request.POST.get("start_date")
            message = request.POST.get("message")
        except (TypeError, ValueError) as exp:
            print(exp)
        if not (days_off <= 0 or not start_date):
            print(request.user)
            leave_request = LeaveRequest(
                employee=request.user, days_off=days_off, starting_date=start_date, message=message)
            leave_request.save()
            messages.success(
                request, 'Your leave request has been sent sucessfully!', extra_tags="success")
        else:
            messages.error(
                request, 'Your form has an error!', extra_tags="error")
    return render(request, template_name='pages/user/request-leave.html')


@login_required(login_url='/account/login')
@csrf_exempt
def register_attendance(request):
    form = AttendanceForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            code = form.cleaned_data["code"]
            latitude = form.cleaned_data["latitude"]
            longitude = form.cleaned_data["longitude"]

            location = Location.objects.filter(code=code).first()
            print(location)
            employee = request.user
            clock_out_time = datetime.now().time()

            attendance = Attendance.objects.filter(
                employee=employee, date=date.today()).first()

            if not position_within_area((latitude, longitude),
                                        (location.latitude,
                                         location.longitude),
                                        location.radius):
                print((latitude, longitude))
                return JsonResponse({"success": False, "message": "You are clocking your attendance off premises. This is improper conduct."})

            if attendance is not None and attendance.clock_out_time:
                return JsonResponse({"success": True, "message": "You have already clocked in and out for today"})

            if attendance is not None:  # meaning the user has clocked in already
                attendance.clock_out_time = clock_out_time
                attendance.save()
                return JsonResponse({"success": True, "message": "You have successfully out for today"})

                # send clock out success message

            # check if all values are valid first
            attendance = Attendance.objects.create(
                location=location,
                employee=employee,
                # clocked in time is filled automatically
                clock_out_time=None
            )
            attendance.save()
            return JsonResponse({"success": True, "message": "You have successfully in for today"})
        return JsonResponse({"success": False, "message": 'You have errors in your form'})
        # check that location matches geolocation of location with the current code
    context = {"form": form}
    return render(request, template_name='pages/user/clock-action.html', context=context)


# not found page
def error_404_view(request, exception):
    return render(request, 'pages/404.html', context={'exception': exception})
