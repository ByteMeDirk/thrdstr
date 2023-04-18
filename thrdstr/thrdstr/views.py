from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserSignupForm, UserEditForm


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


@login_required
def edit_profile_view(request):
    """
    A view that handles the edit profile process.
    The users avatar is cropped and compressed to keep it small.
    """
    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserEditForm(instance=request.user)
    return render(request, "registration/profile.html", {"form": form})
