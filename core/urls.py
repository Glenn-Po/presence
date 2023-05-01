from django.urls import path
from .views import index, render_user_dashboard, \
    render_clocking, render_admin_dashboard, \
    view_locations, view_employees, view_attendances

urlpatterns = [
    path('', index, name="home"),
    path('employee/dashboard', render_user_dashboard, name="user_dashboard"),
    path('employee/dashboard/clock', render_clocking, name="user_clock_action"),
    path('manager/dashboard', render_admin_dashboard, name="admin_dashboard"),
    path('manager/dashboard/locations', view_locations, name="admin_dashboard_locations"),
    path('manager/dashboard/employees', view_employees, name="admin_dashboard_employees"),
    path('manager/dashboard/attendances', view_attendances, name="admin_dashboard_attendances")
]