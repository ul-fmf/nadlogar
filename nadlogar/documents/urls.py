from django.urls import include, path

from . import views

app_name = "documents"
urlpatterns = [
    path("create/", views.create_document, name="create_document"),
    path("<int:document_id>/", views.view_document, name="view_document"),
    path("<int:document_id>/edit/", views.edit_document, name="edit_document"),
    path("<int:document_id>/delete/", views.delete_document, name="delete_document"),
    path("<int:document_id>/problems/", include("problems.urls")),
    path("<int:document_id>/download/", views.preview, name="preview"),
    path("<int:document_id>/download/tex/", views.download_tex, name="download_tex"),
    path("<int:document_id>/download/pdf/", views.download_pdf, name="download_pdf"),
]
