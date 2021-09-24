from django.contrib import admin
from problems.admin import ProblemInline

from .models import Document, DocumentSort, Template


class TemplateInline(admin.TabularInline):
    model = Template
    extra = 2


class DocumentSortAdmin(admin.ModelAdmin):
    inlines = [TemplateInline]


admin.site.register(DocumentSort, DocumentSortAdmin)


class DocumentAdmin(admin.ModelAdmin):
    inlines = [ProblemInline]


admin.site.register(Document, DocumentAdmin)
