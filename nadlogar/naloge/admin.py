from django.contrib import admin
from .models import Naloga


class NalogaInline(admin.TabularInline):
    model = Naloga
    extra = 2
