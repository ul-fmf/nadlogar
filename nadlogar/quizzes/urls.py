from django.urls import path

from . import views

app_name = "quizzes"
urlpatterns = [
    path("create/", views.create_quiz, name="create_quiz"),
    path("<int:quiz_id>/", views.view_quiz, name="view_quiz"),
    path("<int:quiz_id>/edit/", views.edit_quiz, name="edit_quiz"),
    path("<int:quiz_id>/delete/", views.delete_quiz, name="delete_quiz"),
    path("<int:quiz_id>/generate/", views.generate, name="generate"),
]
