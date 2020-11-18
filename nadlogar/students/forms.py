from django.forms import ModelForm

from .models import Student, StudentGroup


class StudentGroupForm(ModelForm):
    class Meta:
        model = StudentGroup
        exclude = []


class StudentForm(ModelForm):
    class Meta:
        model = Student
        exclude = []
