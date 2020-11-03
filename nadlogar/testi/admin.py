from django.contrib import admin

from naloge.admin import NalogaInline
from .models import Test


class TestAdmin(admin.ModelAdmin):
    inlines = [NalogaInline]


admin.site.register(Test, TestAdmin)
