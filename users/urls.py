from django.urls import path

from .views import login_view, logout_view


urlpatterns = [
    path('account/login', login_view, name="login"),
    path('account/logout', logout_view, name="logout")
]
