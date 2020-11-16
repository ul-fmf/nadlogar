from django.urls import path

from . import views

app_name = "quizzes"
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:quiz_id>/", views.details, name="details"),
    path("<int:quiz_id>/edit/", views.edit, name="edit"),
    path("<int:quiz_id>/delete/", views.delete, name="delete"),
    path("<int:quiz_id>/generate/", views.generate, name="generate"),
]
