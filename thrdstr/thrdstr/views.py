import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import (
    UserSignupForm,
    UserEditForm,
    GroupCreateForm,
    GroupEditForm,
    PostCreateForm,
    PostEditForm,
)
from .models import Group, User, Post


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
            form = form.save(commit=False)

            # Check if avatar has been cleared
            if "avatar-clear" in request.POST:
                form.avatar.delete()
                form.avatar = User._meta.get_field("avatar").get_default()

            form.user = request.user
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
    subscribed_groups = Group.objects.filter(users=request.user)

    # list groups made within the last week
    groups_last_week = Group.objects.filter(
        date_created__gte=datetime.datetime.now() - datetime.timedelta(days=7)
    )

    return render(
        request,
        "groups.html",
        {
            "groups": groups,
            "subscribed_groups": subscribed_groups,
            "groups_last_week": groups_last_week,
        },
    )


def groups_user(request):
    """
    List all groups that belong to the user, or the groups that they have subscribed to.
    """
    groups = Group.objects.filter(owner=request.user)
    subscribed_groups = Group.objects.filter(users=request.user)
    return render(
        request,
        "groups/groups_user.html",
        {"groups": groups, "subscribed_groups": subscribed_groups},
    )


def groups_subscribe(request, pk):
    """
    Users can subscribe to a group by clicking on the subscribe button.
    If the user is not subscribed, a subscribe button should be shown,
    and if the user is subscribed, an unsubscribe button should be shown.
    """
    group = Group.objects.get(pk=pk)
    group.users.add(request.user)
    return redirect("groups")


def groups_unsubscribe(request, pk):
    """
    Users can unsubscribe from a group by clicking on the unsubscribe button.
    """
    group = Group.objects.get(pk=pk)
    group.users.remove(request.user)
    return redirect("groups")


@login_required
def groups_create(request):
    """
    Users can create and delete groups.
    If they create a group, they are automatically subscribed to it.
    """
    if request.method == "POST":
        form = GroupCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.save()
            form.users.add(request.user)
            return redirect("groups_user")
    else:
        form = GroupCreateForm()
    return render(request, "groups/groups_create.html", {"form": form})


@login_required
def groups_edit(request, pk):
    group = Group.objects.get(pk=pk)
    if request.method == "POST":
        form = GroupEditForm(request.POST, request.FILES, instance=group)

        if form.is_valid():
            form = form.save(commit=False)

            # Check if banner has been cleared
            if "banner-clear" in request.POST:
                form.banner.delete()
                form.banner = Group._meta.get_field("banner").get_default()

            form.save()
            return redirect("groups_edit", pk=pk)
    else:
        form = GroupEditForm(instance=group)
    return render(request, "groups/groups_edit.html", {"form": form})


@login_required
def groups_delete(request, pk):
    group = Group.objects.get(pk=pk)
    if request.method == "POST":
        group.delete()

    return redirect("groups_user")


# Post Views    ---------------------------------------------------------------
@login_required
def post_list(request, pk):
    """
    Users can view all posts within a specific group that they belong to.
    """
    group = Group.objects.get(pk=pk)
    posts = Post.objects.filter(group=group).order_by("-date_created")
    return render(request, "posts/post_list.html", {"posts": posts, "group": group})


@login_required
def post_create(request, pk=None):
    """
    Users can create a post and select what group it belongs to.

    If pk is not none, the form is pre-populated with the group that the user
    wants to post to.
    The user id is also added to the post.
    """
    if pk is not None:
        group = Group.objects.get(pk=pk)
    else:
        group = None

    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.group = group
            form.save()
            return redirect("post_list", pk=pk)
    else:
        form = PostCreateForm()
    return render(request, "posts/post_create.html", {"form": form, "group": group})


@login_required
def post_edit(request, post_id, group_id):
    """
    Users can edit their own posts.
    """
    post = Post.objects.get(pk=post_id)
    if request.method == "POST":
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect("post_list", pk=group_id)
    else:
        form = PostEditForm(instance=post)
    return render(request, "posts/post_edit.html", {"form": form})


@login_required
def post_delete(request, post_id, group_id):
    """
    Users can delete their own posts.
    """
    post = Post.objects.get(pk=post_id)
    if request.method == "POST":
        post.delete()
    return redirect("post_list", pk=group_id)


@login_required
def post_like(request, post_id):
    """
    Users can like posts, this makes use of AJAX to
    prevent the page from reloading.
    """
    post = Post.objects.get(pk=post_id)
    post.likes.add(request.user)
    return JsonResponse({"likes": post.likes.count()})


@login_required
def post_unlike(request, post_id):
    """
    Users can unlike posts.
    """
    post = Post.objects.get(pk=post_id)
    post.likes.remove(request.user)
    return JsonResponse({"likes": post.likes.count()})
