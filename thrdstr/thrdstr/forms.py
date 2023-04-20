from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Group, Post


# User Forms ------------------------------------------------------------------
class UserSignupForm(UserCreationForm):
    """
    A form that handles the sign up process.
    """

    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date", "placeholder": "YYYY-MM-DD"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "date_of_birth", "password1", "password2")


class UserEditForm(forms.ModelForm):
    """
    A form that allows a user to edit their profile.
    """

    avatar = forms.ImageField(required=False)
    bio = forms.CharField(max_length=500, required=False)
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date", "placeholder": "YYYY-MM-DD"}),
    )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("avatar", "bio", "date_of_birth", "first_name", "last_name")


# Group Forms -----------------------------------------------------------------
class GroupCreateForm(forms.ModelForm):
    """
    A form that allows a user to create a group.
    """

    banner = forms.ImageField(required=False)
    description = forms.CharField(max_length=500, required=False)

    class Meta:
        model = Group
        fields = ("banner", "name", "description")


class GroupEditForm(forms.ModelForm):
    """
    A form that allows a user to edit a group.
    """

    banner = forms.ImageField(required=False)
    description = forms.CharField(max_length=500, required=False)

    class Meta:
        model = Group
        fields = ("banner", "description")


# Post Forms ------------------------------------------------------------------
class PostCreateForm(forms.ModelForm):
    """
    A form that allows a user to create a post.
    """

    body = forms.CharField(max_length=500, required=False)

    class Meta:
        model = Post
        fields = ("title", "body", "image", "file")


class PostEditForm(forms.ModelForm):
    """
    A form that allows a user to edit a post.
    If the post has been edited, the edited field will be set to True.
    """

    body = forms.CharField(max_length=500, required=False)

    class Meta:
        model = Post
        fields = ("title", "body", "image", "file")
