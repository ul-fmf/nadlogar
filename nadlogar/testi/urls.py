from django.urls import path

from . import views

app_name = "testi"
urlpatterns = [
    path("", views.seznam, name="seznam"),
    path("<int:id>/", views.podrobnosti, name="podrobnosti"),
    path("<int:id>/nadloga/", views.nadloga, name="nadloga"),
    path("dodaj/", views.dodaj, name="dodaj"),
    path("<int:id>/uredi/", views.uredi, name="uredi"),
    path("<int:id>/pobrisi/", views.pobrisi, name="pobrisi"),
]
