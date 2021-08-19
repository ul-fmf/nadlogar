from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="homepage.html"), name="homepage"),
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
    path("problems/", include("problems.urls")),
    path("quizzes/", include("quizzes.urls")),
    path("students/", include("students.urls")),
]
