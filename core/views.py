from django.shortcuts import render


def index(request):
    return render(request, template_name='pages/index.html')


def render_user_dashboard(request):
    return render(request, template_name="pages/user/dashboard.html")


def render_clocking(request):
    if request.method == "POST":
        pass
    clock_type = request.GET.get("type")
    return render(request, template_name='pages/user/clock-action.html', context={'clock': clock_type})


# location
def create_location(req):
    return render('')


# attendance
def register_attendance(request):
    if request.user.is_authenticated:
        # check that location matches geolocation of location with the current code
        return
