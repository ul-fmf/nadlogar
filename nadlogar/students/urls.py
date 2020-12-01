from django.urls import path

from . import views

app_name = "students"
urlpatterns = [
    path("create/", views.create_group, name="create_group"),
    path("<int:group_id>/", views.view_group, name="view_group"),
    path("<int:group_id>/edit/", views.edit_group, name="edit_group"),
    path("<int:group_id>/delete/", views.delete_group, name="delete_group"),
    path("student/create/", views.create_student, name="create_student"),
    path(
        "student/<int:student_id>/edit/",
        views.edit_student,
        name="edit_student",
    ),
    path(
        "student/<int:student_id>/delete/",
        views.delete_student,
        name="delete_student",
    ),
]
