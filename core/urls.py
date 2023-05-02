from django.urls import path
from .views import index, render_user_dashboard, render_admin_dashboard, \
    view_locations, create_location, update_location, delete_location,\
    view_employees, create_employee, update_employee, delete_employee, view_employee,\
    view_attendance, filter_attendance_by_date, filter_attendance_by_employee,\
    register_attendance, delete_leave_request, request_leave

urlpatterns = [
    path('', index, name="home"),
    # employee routes
    path('employee/dashboard', render_user_dashboard, name="user_dashboard"),
    path('employee/dashboard/clock', register_attendance, name="user_clock_action"),
    path('employee/dashboard/request-leave',
         request_leave, name="request_leave"),

    # manager routes
    # dashboard-home
    path('manager/dashboard', render_admin_dashboard, name="admin_dashboard"),
    path('manager/dashboard/delete/<int:id>/',
         delete_leave_request, name="delete_leave_request"),

    # dashboard-locations
    path('manager/dashboard/locations', view_locations,
         name="admin_dashboard_locations"),
    path('manager/dashboard/locations/new', create_location,
         name="admin_dashboard_locations_new"),
    path('manager/dashboard/locations/update/<int:id>/', update_location,
         name="admin_dashboard_locations_update"),
    path('manager/dashboard/locations/delete/<int:id>/', delete_location,
         name="admin_dashboard_locations_delete"),

    # dashboard-locations
    path('manager/dashboard/employees', view_employees,
         name="admin_dashboard_employees"),
    path('manager/dashboard/employees/new', create_employee,
         name="admin_dashboard_employees_new"),
    path("manager/dashboard/employees/update/<int:id>/", update_employee,
         name="admin_dashboard_employees_update"),
    path('manager/dashboard/employees/view/<int:id>/', view_employee,
         name="admin_dashboard_employees_view"),
    path('manager/dashboard/employees/delete/<int:id>/', delete_employee,
         name="admin_dashboard_employees_delete"),

    # dashboard attendanced: filter,
    path('manager/dashboard/attendances', view_attendance,
         name="admin_dashboard_attendances"),
    path('manager/dashboard/attendances/filter/<str:date>/', filter_attendance_by_date,
         name="admin_dashboard_attendances_filter_date"),
    path('manager/dashboard/attendances/filter/<int:id>/', filter_attendance_by_employee,
         name="admin_dashboard_attendances_filter_employee")
]
