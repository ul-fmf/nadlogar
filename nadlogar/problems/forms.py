from django import forms
from django.contrib.contenttypes.models import ContentType
from quizzes.models import Quiz

from .models import ProblemText, limit_content_type_choices


class ProblemForm(forms.Form):
    quiz = forms.ModelChoiceField(
        queryset=Quiz.objects.all(), widget=forms.HiddenInput()
    )
    content_type = forms.ModelChoiceField(queryset=ContentType.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content_type"].queryset = ContentType.objects.filter(
            **limit_content_type_choices()
        )


def problem_parameters_form(content_type, *args, **kwargs):
    class ProblemParametersForm(forms.ModelForm):
        class Meta:
            model = content_type.model_class()
            exclude = ["text"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["quiz"].widget = forms.HiddenInput()
            self.fields["content_type"].widget = forms.HiddenInput()

    return ProblemParametersForm(*args, **kwargs)


def problem_text_form(content_type, *args, **kwargs):
    class ProblemTextForm(forms.ModelForm):
        class Meta:
            model = content_type.model_class()
            exclude = []

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name in self.fields:
                if field_name != "text":
                    self.fields[field_name].widget = forms.HiddenInput()
            self.fields["text"].queryset = content_type.problemtext_set

    return ProblemTextForm(*args, **kwargs)
