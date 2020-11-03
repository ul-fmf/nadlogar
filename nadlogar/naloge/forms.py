from django.forms import ModelForm

from .models import Naloga

class NalogaForm(ModelForm):
    class Meta:
        model = Naloga
        exclude = ['test']
