from django import forms


class AttendanceForm(forms.Form):
    latitude = forms.DecimalField(max_digits=8, decimal_places=4)
    longitude = forms.DecimalField(max_digits=8, decimal_places=4)
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
    is_manager = forms.BooleanField(initial=False)
