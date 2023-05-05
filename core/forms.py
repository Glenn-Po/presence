from django import forms

from core.models import Location


class AttendanceForm(forms.Form):
    latitude = forms.DecimalField(max_digits=20, decimal_places=8)
    longitude = forms.DecimalField(max_digits=20, decimal_places=8)
    code = forms.CharField(max_length=128)


class EmployeeForm(forms.Form):
    email = forms.EmailField(required=True, empty_value=False)
    password = forms.CharField(widget=forms.PasswordInput)
    cpassword = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=100)
    role = forms.CharField(max_length=100)
    dob = forms.DateField()
    start_date = forms.DateField()
    telephone = forms.CharField(max_length=15)
    address = forms.CharField(max_length=255)
    is_manager = forms.BooleanField(initial=False, required=False)


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ("name", "radius", "latitude", "longitude")

# class LeaveRequest(forms.ModelForm):
#     employee = models.ForeignKey(
#         CustomUser, related_name="leave_request", on_delete=models.CASCADE)
#     days_off = models.IntegerField(null=False)
#     starting_date = models.DateField(null=False)
#     message = models.TextField(max_length=2048, blank=True, null=True)
