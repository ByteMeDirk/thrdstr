"""
URL configuration for thrdstr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings
from .views import index, SignupView, edit_profile_view, groups, groups_create, groups_edit, groups_delete

admin.autodiscover()

urlpatterns = [
    # Root URLs
    path(r"", index, name="index"),
    path("admin/", admin.site.urls),

    # User URLs
    path(
        "accounts/", include("django.contrib.auth.urls")
    ),  # This is for the login and logout views
    path("accounts/signup/", SignupView.as_view(), name="signup"),
    path("accounts/profile/", edit_profile_view, name="profile"),

    # Groups URLs
    path("groups/", groups, name="groups"),
    path("groups/create/", groups_create, name="groups_create"),
    path("groups/edit/<int:pk>/", groups_edit, name="groups_edit"),
    path("groups/delete/<int:pk>/", groups_delete, name="groups_delete")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
