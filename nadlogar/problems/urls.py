from django.urls import path

from . import views

app_name = "problems"
urlpatterns = [
    path("choose/<int:document_id>/", views.choose_problem, name="choose_problem"),
    path("create/", views.create_problem, name="create_problem"),
    path(
        "<int:problem_id>/edit/",
        views.edit_problem,
        name="edit_problem",
    ),
    path("<int:problem_id>/delete/", views.delete_problem, name="delete_problem"),
]
