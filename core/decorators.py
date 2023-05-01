from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test


def authorize_manager_only(function=None, redirect_url="/login"):
    def check_profile(user):
        return user.profile.is_manager
    # use user_passes_test decorator with check_profile function
    actual_decorator = user_passes_test(check_profile, login_url=redirect_url)
    # apply the decorator to the view function
    if function:
        return actual_decorator(function)
    return actual_decorator
