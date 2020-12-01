from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="homepage.html"), name="homepage"),
    path("admin/", admin.site.urls),
    path("problems/", include("problems.urls")),
    path("quizzes/", include("quizzes.urls")),
    path("students/", include("students.urls")),
]
