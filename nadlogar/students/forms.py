from django.forms import ModelForm

from .models import Student, StudentGroup


class StudentGroupForm(ModelForm):
    class Meta:
        model = StudentGroup
        exclude = ["user"]


class StudentForm(ModelForm):
    class Meta:
        model = Student
        exclude = ["group"]
