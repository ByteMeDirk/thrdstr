from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class User(AbstractUser, PermissionsMixin):
    """
    User model that extends and modifies the BaseUserManager.
    """
    username = models.CharField(max_length=100, unique=True)
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)

