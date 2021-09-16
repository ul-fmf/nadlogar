from django.contrib import admin
from problems.admin import ProblemInline

from .models import Document


class DocumentAdmin(admin.ModelAdmin):
    inlines = [ProblemInline]


admin.site.register(Document, DocumentAdmin)
