from django.forms import ModelForm

from .models import Student, StudentGroup


class StudentGroupForm(ModelForm):
    class Meta:
        model = StudentGroup
        exclude = ["user"]


class StudentForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group"].queryset = user.studentgroup_set.all()

    class Meta:
        model = Student
        exclude = []
