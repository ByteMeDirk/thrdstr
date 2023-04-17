from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


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
