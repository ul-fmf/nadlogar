from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("problems/", include("problems.urls")),
    path("quizzes/", include("quizzes.urls")),
]
