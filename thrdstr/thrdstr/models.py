import datetime

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class User(AbstractUser, PermissionsMixin):
    """
    User model that extends and modifies the BaseUserManager.
    """

    username = models.CharField(max_length=100, unique=True)
    avatar = models.ImageField(
        upload_to="avatars", null=True, blank=False, default="avatars/default.jpg"
    )
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
    date_joined = models.DateTimeField(default=datetime.datetime.now)


class Group(models.Model):
    """
    Users can create a group or subscribe to groups and post in them.
    They can also unsubscribe from groups. There needs to be a relationship
    between multiple users subscribed to any given group.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    banner = models.ImageField(
        upload_to="group_banners",
        null=True,
        blank=True,
        default="group_banners/default.jpg",
    )
    users = models.ManyToManyField(User, related_name="subscribed_groups")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="group_owner",
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(default=datetime.datetime.now)

    # return group name as string
    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Users can create a post in a group and other users can comment on it.
    """

    title = models.CharField(max_length=100, null=True, blank=True)
    body = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user")
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="post_group"
    )
    image = models.ImageField(
        upload_to="post_image",
        null=True,
        blank=True,
    )
    file = models.FileField(
        upload_to="post_file",
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(default=datetime.datetime.now)
    date_updated = models.DateTimeField(default=datetime.datetime.now)

    # edited field is true if the post has been edited
    edited = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name="post_likes")
