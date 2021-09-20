from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms.models import ModelChoiceIterator
from documents.models import Document

from .models import ProblemText, limit_content_type_choices


def problem_form(content_type, *args, **kwargs):
    Generator = content_type.model_class()
    example_problem = Generator()
    example_data = example_problem.generate_data(None)

    class ProblemTextChoiceIterator(ModelChoiceIterator):
        def choice(self, obj):
            return (self.field.prepare_value(obj), obj.render(example_data))

    class ProblemForm(forms.ModelForm):
        class Meta:
            model = Generator
            exclude = ["content_type", "document"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["text"].queryset = content_type.problemtext_set
            self.fields["text"].iterator = ProblemTextChoiceIterator
            self.fields["text"].empty_label = None
            self.fields["text"].custom_display = True

    return ProblemForm(*args, **kwargs)
