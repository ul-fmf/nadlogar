from django.urls import path

from . import views

app_name = "documents"
urlpatterns = [
    path("create/", views.create_document, name="create_document"),
    path("<int:document_id>/", views.view_document, name="view_document"),
    path("<int:document_id>/edit/", views.edit_document, name="edit_document"),
    path("<int:document_id>/delete/", views.delete_document, name="delete_document"),
    path("<int:document_id>/generate/", views.generate, name="generate"),
]
