from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import normalize_newlines


def problem_form(content_type, *args, **kwargs):
    """Returns a form for editing a problem.

    The form is generated dynamically based on the problem generator class. The
    form is used for both creating a new problem and editing an existing one."""

    Generator = content_type.model_class()

    class ProblemForm(forms.ModelForm):
        """A form for editing a problem.

        This form is used for editing a problem. It is used for both creating a new
        problem and editing an existing one. The form is generated dynamically based
        on the problem generator class."""

        # We add a field for allowing the user to choose default or custom text.
        uses_custom_text = forms.BooleanField(initial=False, required=False)

        class Meta:
            model = Generator
            # We exclude the content type and document fields, because they are
            # automatically set when the problem is saved.
            exclude = ["content_type", "document"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            instance_uses_custom_text = self.instance.uses_custom_text()
            # This reflects the choice the user made in the previous step.
            user_wants_custom_text = self.data.get("uses_custom_text") != "false"
            # If the instance does not use custom text, we set the initial values
            # for the instruction and solution fields to the default values.
            if not instance_uses_custom_text:
                self.initial["instruction"] = Generator.default_instruction
                self.initial["solution"] = Generator.default_solution
            self.initial["uses_custom_text"] = (
                instance_uses_custom_text and user_wants_custom_text
            )
            # We set the custom_display attribute on all fields that are not
            # displayed together with other problem parameters.
            for field_name in ["uses_custom_text", "instruction", "solution"]:
                self.fields[field_name].custom_display = True

        def clean(self):
            super().clean()
            errors = {}
            if self.cleaned_data["uses_custom_text"]:
                # If the user wants to use custom text, we ensure that the
                # instruction and solution fields are not empty.
                for field_name in ["instruction", "solution"]:
                    if not self.cleaned_data[field_name]:
                        errors[
                            field_name
                        ] = "Ob izbiri novega besedila mora biti to polje neprazno."
            else:
                # If the user does not want to use custom text, we ensure that the
                # instruction and solution fields are empty or equal to the default
                # values.
                def _erase_if_equal(field, default):
                    normalized_value = normalize_newlines(self.cleaned_data[field])
                    normalized_default = normalize_newlines(default)
                    if normalized_value == normalized_default:
                        self.cleaned_data[field] = ""

                _erase_if_equal("instruction", Generator.default_instruction)
                _erase_if_equal("solution", Generator.default_solution)
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
            """Returns True if the parameter form should be displayed."""
            return any(
                not getattr(field.field, "custom_display", False)
                for field in self.visible_fields()
            )

    return ProblemForm(*args, **kwargs)
