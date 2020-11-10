from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("naloge/", include("naloge.urls")),
    path("testi/", include("testi.urls")),
]
