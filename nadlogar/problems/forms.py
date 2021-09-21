from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
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
        question = forms.CharField(
            label="Vprašanje", widget=forms.Textarea(attrs={"rows": 5}), required=False
        )
        answer = forms.CharField(
            label="Odgovor", widget=forms.Textarea(attrs={"rows": 3}), required=False
        )

        class Meta:
            model = Generator
            exclude = ["content_type", "document"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["text"].queryset = content_type.problemtext_set
            self.fields["text"].iterator = ProblemTextChoiceIterator
            self.fields["text"].empty_label = None
            for field_name in ["text", "question", "answer"]:
                self.fields[field_name].custom_display = True

        def clean(self):
            cleaned_data = super().clean()
            errors = {}
            if "text" in cleaned_data:
                for field_name in ["question", "answer"]:
                    if cleaned_data[field_name]:
                        errors[
                            field_name
                        ] = "Da ne bi prišlo do izgube podatkov, mora biti ob izbiri obstoječega besedila to polje prazno."
            else:
                del self.errors["text"]
                for field_name in ["question", "answer"]:
                    if not cleaned_data[field_name]:
                        errors[
                            field_name
                        ] = "Ob izbiri novega besedila mora biti to polje neprazno."
            if errors:
                raise ValidationError(errors)

        def save(self, commit=True):
            problem = super().save(commit=False)
            if "text" not in self.cleaned_data:
                text = ProblemText.objects.create(
                    content_type=problem.content_type,
                    question=self.cleaned_data["question"],
                    answer=self.cleaned_data["answer"],
                )
                problem.text = text
            if commit:
                problem.save()
            return problem

    return ProblemForm(*args, **kwargs)
