from django.contrib import admin

from .models import Problem


class ProblemInline(admin.TabularInline):
    model = Problem
    extra = 2
