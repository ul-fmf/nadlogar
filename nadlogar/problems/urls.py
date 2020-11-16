from django.urls import path

from . import views

app_name = "problems"
urlpatterns = [
    path("create/", views.create, name="create"),
    path("<int:problem_id>/", views.details, name="details"),
    path(
        "<int:problem_id>/edit/parameters/",
        views.edit_parameters,
        name="edit_parameters",
    ),
    path("<int:problem_id>/edit/text/", views.edit_text, name="edit_text"),
    path("<int:problem_id>/delete/", views.delete, name="delete"),
]
