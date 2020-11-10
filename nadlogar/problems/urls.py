from django.urls import path

from . import views

app_name = "problems"
urlpatterns = [
    path("<int:problem_id>/", views.details, name="details"),
    path("create/<int:quiz_id>/", views.choose_generator, name="choose_generator"),
    path("create/<int:quiz_id>/<int:content_type_id>/", views.create, name="create"),
    path("<int:problem_id>/edit/", views.edit, name="edit"),
    path("<int:problem_id>/delete/", views.delete, name="delete"),
]
