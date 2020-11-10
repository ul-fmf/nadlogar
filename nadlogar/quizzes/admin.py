from django.contrib import admin
from problems.admin import ProblemInline

from .models import Quiz


class QuizAdmin(admin.ModelAdmin):
    inlines = [ProblemInline]


admin.site.register(Quiz, QuizAdmin)
