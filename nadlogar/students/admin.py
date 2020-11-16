from django.contrib import admin

from .models import Student, StudentGroup


class StudentInline(admin.TabularInline):
    model = Student
    extra = 3


class StudentGroupAdmin(admin.ModelAdmin):
    inlines = [StudentInline]


admin.site.register(StudentGroup, StudentGroupAdmin)
