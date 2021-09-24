from django.forms import ModelForm
from django.forms.widgets import DateInput

from .models import Document


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        exclude = ["student_group"]
        widgets = {
            "date": DateInput(attrs={"type": "date"}),
        }
