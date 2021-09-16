from django.forms import ModelForm

from .models import Document


class DocumentForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student_group"].queryset = user.studentgroup_set.all()

    class Meta:
        model = Document
        exclude = []
