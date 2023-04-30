from django.urls import path
from .views import index, render_user_dashboard, render_clocking

urlpatterns = [
    path('', index, name="home"),
    path('employee/dashboard', render_user_dashboard, name="user_dashboard"),
    path('employee/dashboard/clock', render_clocking, name="user_clock_action")
]