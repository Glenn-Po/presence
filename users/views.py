from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email, password)
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.profile__is_manager:
                    return redirect('manager/dashboard')
                return redirect('employee/dashboard')
            else:
                error = 'Invalid email or password'
        else:
            error = 'Email and password are required'
        return render(request, 'pages/login.html', context={'error': error})
    else:
        return render(request, 'pages/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')
