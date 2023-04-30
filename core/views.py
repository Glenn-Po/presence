from django.shortcuts import render


def index(request):
    return render(request, template_name='pages/index.html')
# location
def create_location(req):
    return render('')


#attendance
def register_attendance(request):
    if request.user.is_authenticated:
        # check that location matches geolocation of location with the current code
        return
