from django.urls import path

from . import views

app_name = 'naloge'
urlpatterns = [
    path('<int:id>/', views.podrobnosti, name='podrobnosti'),
    path('<int:id>/primer/', views.primer, name='primer'),
    path('dodaj/<int:test_id>/', views.dodaj, name='dodaj'),
    path('<int:id>/uredi/', views.uredi, name='uredi'),
    path('<int:id>/pobrisi/', views.pobrisi, name='pobrisi'),
]
