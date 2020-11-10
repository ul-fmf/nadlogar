from django.forms import ModelForm

from .models import Naloga, KrajsanjeUlomkov, IskanjeNicelPolinoma


class NalogaForm(ModelForm):
    class Meta:
        model = Naloga
        exclude = ['content_type', 'test']

    @classmethod
    def obrazec_modela(cls, model):
        for naloga_form in cls.__subclasses__():
            if naloga_form.Meta.model == model:
                return naloga_form
        return cls
    
    @classmethod
    def obrazec_naloge(cls, naloga):
        return cls.obrazec_modela(type(naloga))
    

class KrajsanjeUlomkovForm(NalogaForm):
    class Meta(NalogaForm.Meta):
        model = KrajsanjeUlomkov


class IskanjeNicelPolinomaForm(NalogaForm):
    class Meta(NalogaForm.Meta):
        model = IskanjeNicelPolinoma
