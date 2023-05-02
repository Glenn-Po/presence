from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=100,)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=100,)
    start_date = models.DateField(auto_now=True)
    telephone = models.CharField(max_length=16)
    address = models.CharField(max_length=255)
    is_manager = models.BooleanField(default=False, )

    def __str__(self):
        return self.name


# Automatically creating the user's profile when the user is created
# @receiver(post_save, sender=CustomUser)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=CustomUser)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()
