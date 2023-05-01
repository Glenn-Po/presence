from django.urls import path
from .views import index, render_user_dashboard, render_admin_dashboard, \
    view_locations, view_employees, attendances_view, register_attendance,\
    delete_leave_request

urlpatterns = [
    path('', index, name="home"),

    # employee routes
    path('employee/dashboard', render_user_dashboard, name="user_dashboard"),
    path('employee/dashboard/clock', register_attendance, name="user_clock_action"),

    # manager routes
    # dashboard-home
    path('manager/dashboard', render_admin_dashboard, name="admin_dashboard"),
    path('manager/dashboard/request/:id',
         delete_leave_request, name="delete_leave_request"),

    # dashboard-locations
    path('manager/dashboard/locations', view_locations,
         name="admin_dashboard_locations"),

    path('manager/dashboard/employees', view_employees,
         name="admin_dashboard_employees"),
    path('manager/dashboard/attendances', attendances_view,
         name="admin_dashboard_attendances")
]
