from django.contrib import admin
from problems.admin import ProblemInline

from .models import Document, Template

admin.site.register(Template)


class DocumentAdmin(admin.ModelAdmin):
    inlines = [ProblemInline]


admin.site.register(Document, DocumentAdmin)
