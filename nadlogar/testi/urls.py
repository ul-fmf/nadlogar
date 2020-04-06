from django.urls import path

from . import views

app_name = 'testi'
urlpatterns = [
    # ex: /testi/
    path('', views.index, name='index'),
    # ex: /testi/5/
    path('<int:pk>/', views.podrobnosti, name='podrobnosti'),
    # ex: /testi/5/nadloga
    path('<int:pk>/nadloga/', views.nadloga, name='nadloga'),
]
