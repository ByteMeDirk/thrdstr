from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserSignupForm


# Root Views    ---------------------------------------------------------------
def index(request):
    """
    The index view.
    """
    return render(request, "index.html", {})


# User Views    ---------------------------------------------------------------

class SignupView(CreateView):
    """
    A view that handles the sign up process.
    """

    form_class = UserSignupForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
