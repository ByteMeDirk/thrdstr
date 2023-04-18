from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserSignupForm, UserEditForm, GroupCreateForm, GroupEditForm
from .models import Group

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


# Groups Views    ---------------------------------------------------------------
def groups(request):
    """
    List all groups and subscribe or unsubscribe to groups.
    """
    groups = Group.objects.all()
    return render(request, "groups.html", {"groups": groups})


@login_required
def groups_create(request):
    """
    Users can create and delete groups.
    """
    if request.method == "POST":
        form = GroupCreateForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner_id = request.user.id
            group.save()
            return redirect("groups")
    else:
        form = GroupCreateForm()
    return render(request, "groups/groups_create.html", {"form": form})


@login_required
def groups_edit(request, pk):
    """
    Users can edit their groups.
    """
    group = Group.objects.get(id=pk)
    print(group)
    if request.method == "POST":
        form = GroupEditForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            return redirect("groups")
    else:
        form = GroupEditForm(instance=group)
    return render(request, "groups/groups_edit.html", {"form": form})