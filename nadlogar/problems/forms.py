from django import forms
from django.contrib.contenttypes.models import ContentType
from quizzes.models import Quiz

from .models import Problem


class ProblemForm(forms.Form):
    quiz = forms.ModelChoiceField(
        queryset=Quiz.objects.all(), widget=forms.HiddenInput()
    )
    content_type = forms.ModelChoiceField(queryset=ContentType.objects.all())


def problem_parameters_form(cls, *args, **kwargs):
    class ProblemParametersForm(forms.ModelForm):
        class Meta:
            model = cls
            exclude = ["text"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["quiz"].widget = forms.HiddenInput()
            self.fields["content_type"].widget = forms.HiddenInput()

    return ProblemParametersForm(*args, **kwargs)


def problem_text_form(cls, *args, **kwargs):
    class ProblemTextForm(forms.ModelForm):
        class Meta:
            model = cls
            exclude = []

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name in self.fields:
                if field_name != "text":
                    self.fields[field_name].widget = forms.HiddenInput()

    return ProblemTextForm(*args, **kwargs)
