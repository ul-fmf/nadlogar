from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import ModelChoiceIterator

from .models import ProblemText


def problem_form(content_type, *args, **kwargs):
    Generator = content_type.model_class()
    example_problem = Generator()
    example_data = example_problem.generate_data(None, 1)

    class ProblemTextChoiceIterator(ModelChoiceIterator):
        def choice(self, obj):
            return (self.field.prepare_value(obj), obj.render(example_data))

    class ProblemForm(forms.ModelForm):
        instruction = forms.CharField(
            label="Navodilo",
            widget=forms.Textarea(attrs={"rows": 5}),
            required=False,
            initial=Generator.default_instruction,
        )
        solution = forms.CharField(
            label="Rešitev",
            widget=forms.Textarea(attrs={"rows": 3}),
            required=False,
            initial=Generator.default_solution,
        )

        class Meta:
            model = Generator
            exclude = ["content_type", "document"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["text"].queryset = content_type.problemtext_set
            self.fields["text"].iterator = ProblemTextChoiceIterator
            self.fields["text"].empty_label = None
            for field_name in ["text", "instruction", "solution"]:
                self.fields[field_name].custom_display = True

        def clean(self):
            cleaned_data = super().clean()
            errors = {}
            if "text" in cleaned_data:
                for field_name in ["instruction", "solution"]:
                    if cleaned_data[field_name]:
                        errors[field_name] = (
                            "Da ne bi prišlo do izgube podatkov, mora biti ob izbiri"
                            " obstoječega besedila to polje prazno."
                        )
            else:
                del self.errors["text"]
                for field_name in ["instruction", "solution"]:
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
                    instruction=self.cleaned_data["instruction"],
                    solution=self.cleaned_data["solution"],
                )
                problem.text = text
            if commit:
                problem.save()
            return problem

        def display_parameter_form(self):
            return any(
                not getattr(field.field, "custom_display", False)
                for field in self.visible_fields()
            )

    return ProblemForm(*args, **kwargs)
