from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms.models import ModelChoiceIterator
from documents.models import Document

from .models import ProblemText, limit_content_type_choices


class ProblemForm(forms.Form):
    document = forms.ModelChoiceField(
        queryset=Document.objects.all(), widget=forms.HiddenInput()
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
            self.fields["document"].widget = forms.HiddenInput()
            self.fields["content_type"].widget = forms.HiddenInput()

    return ProblemParametersForm(*args, **kwargs)


def problem_text_form(problem, *args, **kwargs):
    data = problem.generate()

    class ProblemTextChoiceIterator(ModelChoiceIterator):
        def choice(self, obj):
            return (self.field.prepare_value(obj), obj.render(data))

    class ProblemTextForm(forms.ModelForm):
        class Meta:
            model = type(problem)
            exclude = []

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name in self.fields:
                if field_name != "text":
                    self.fields[field_name].widget = forms.HiddenInput()
            self.fields["text"].queryset = problem.content_type.problemtext_set
            self.fields["text"].iterator = ProblemTextChoiceIterator
            self.fields["text"].empty_label = None

    return ProblemTextForm(*args, **kwargs)
