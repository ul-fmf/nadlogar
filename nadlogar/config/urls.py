from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from utils import views

urlpatterns = [
    path(
        "",
        views.homepage,
        name="homepage",
    ),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page=settings.LOGIN_URL),
        name="logout",
    ),
    path("admin/", admin.site.urls),
    path("students/", include("students.urls")),
]
