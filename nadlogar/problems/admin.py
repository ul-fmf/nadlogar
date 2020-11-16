from django.contrib import admin

from .models import Problem, ProblemText


class ProblemInline(admin.TabularInline):
    model = Problem
    extra = 2


admin.site.register(ProblemText)
