from django import forms
from django.core.exceptions import ValidationError


def problem_form(content_type, *args, **kwargs):
    Generator = content_type.model_class()

    class ProblemForm(forms.ModelForm):
        uses_custom_text = forms.BooleanField(initial=False, required=False)

        class Meta:
            model = Generator
            exclude = ["content_type", "document"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            instance_uses_custom_text = self.instance.uses_custom_text()
            user_wants_custom_text = self.data.get("uses_custom_text") != "false"
            if not instance_uses_custom_text:
                self.initial["instruction"] = Generator.default_instruction
                self.initial["solution"] = Generator.default_solution
            self.initial["uses_custom_text"] = (
                instance_uses_custom_text and user_wants_custom_text
            )
            for field_name in ["uses_custom_text", "instruction", "solution"]:
                self.fields[field_name].custom_display = True

        def clean(self):
            super().clean()
            errors = {}
            if self.cleaned_data["uses_custom_text"]:
                for field_name in ["instruction", "solution"]:
                    if not self.cleaned_data[field_name]:
                        errors[
                            field_name
                        ] = "Ob izbiri novega besedila mora biti to polje neprazno."
            else:
                if self.cleaned_data["instruction"] == Generator.default_instruction:
                    self.cleaned_data["instruction"] = ""
                if self.cleaned_data["solution"] == Generator.default_solution:
                    self.cleaned_data["solution"] = ""
                for field_name in ["instruction", "solution"]:
                    if self.cleaned_data[field_name]:
                        errors[field_name] = (
                            "Da ne bi prišlo do izgube podatkov, mora biti ob izbiri"
                            " privzetega besedila to polje prazno ali enako privzeti"
                            " vrednosti."
                        )
            if errors:
                raise ValidationError(errors)

        def display_parameter_form(self):
            return any(
                not getattr(field.field, "custom_display", False)
                for field in self.visible_fields()
            )

    return ProblemForm(*args, **kwargs)
