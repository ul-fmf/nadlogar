from django.contrib import admin

from .models import Test
from naloge.models import Naloga


class NalogaInline(admin.TabularInline):
    model = Naloga
    extra = 2


class TestAdmin(admin.ModelAdmin):
    inlines = [NalogaInline]


admin.site.register(Test, TestAdmin)
