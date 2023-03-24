from django.db.models.fields import NOT_PROVIDED
from django.test import TestCase

from .models import Problem


class GeneratorTest(TestCase):
    def test_default_arguments(self):
        """All generators have default values for all parameters.

        This test ensures that all generators have default values for all
        parameters. This is important, because the default values are used when
        generating example data."""
        for generator in Problem.__subclasses__():
            for field in generator._meta.get_fields():
                # We exclude the fields that are not used in generating example data.
                if field.name not in [
                    "id",
                    "document",
                    "content_type",
                    "problem_ptr",
                    "instruction",
                    "solution",
                ]:
                    self.assertNotEqual(
                        field.default,
                        NOT_PROVIDED,
                        f"{generator.__name__}, {field.name}",
                    )

    def test_default_text(self):
        """All generators have default text for the instruction and solution."""
        for generator in Problem.__subclasses__():
            self.assertIsNotNone(generator.default_instruction)
            self.assertIsNotNone(generator.default_solution)

    def test_generate(self):
        """All generators can generate example data."""
        for generator in Problem.__subclasses__():
            # We use example_data instead of generate because generate
            # can fail to produce a valid example on the first attempt.
            generator().example_data()
