from django.urls import path

from . import views

app_name = "problems"
urlpatterns = [
    path("create/<int:content_type_id>/", views.create_problem, name="create_problem"),
    path("create/", views.choose_problem, name="choose_problem"),
    path(
        "<int:problem_id>/edit/",
        views.edit_problem,
        name="edit_problem",
    ),
    path("<int:problem_id>/delete/", views.delete_problem, name="delete_problem"),
    path(
        "<int:problem_id>/duplicate/", views.duplicate_problem, name="duplicate_problem"
    ),
]
