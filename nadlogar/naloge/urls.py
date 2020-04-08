from django.urls import path

from . import views

app_name = 'naloge'
urlpatterns = [
    # primer: /naloge/
    path('', views.index, name='index'),
    # primer: /naloge/5/
    path('<int:pk>/', views.podrobnosti, name='podrobnosti'),
    # primer: /naloge/5/primer/
    path('<int:pk>/primer/', views.primer, name='primer'),
]
