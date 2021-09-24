from django.forms import ModelForm

from .models import StudentGroup


class StudentGroupForm(ModelForm):
    class Meta:
        model = StudentGroup
        exclude = ["user"]
