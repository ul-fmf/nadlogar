from django.db.models.fields import NOT_PROVIDED
from django.test import TestCase
from model_bakery import baker

from .models import Problem


class ProblemTest(TestCase):
    def setUp(self):
        self.number_of_subproblems = 100

    def test_krajsanje_ulomkov(self):
        """Generator za krajšanje ulomkov vrne ustrezen slovar"""
        problem = baker.make(
            "KrajsanjeUlomkov", number_of_subproblems=self.number_of_subproblems
        )
        for primer in problem.example_data():
            a = primer.pop("okrajsan_stevec")
            b = primer.pop("okrajsan_imenovalec")
            c = primer.pop("neokrajsan_stevec")
            d = primer.pop("neokrajsan_imenovalec")
            self.assertEqual(primer, {})
            self.assertEqual(a * d, b * c)

    def test_iskanje_nicel_polinoma(self):
        """Generator za iskanje ničel polinoma vrne ustrezen slovar"""
        problem = baker.make(
            "IskanjeNicelPolinoma", number_of_subproblems=self.number_of_subproblems
        )
        for primer in problem.example_data():
            nicle = primer.pop("nicle")
            polinom = primer.pop("polinom")
            self.assertEqual(primer, {})
            self.assertIsInstance(nicle, set)
            self.assertIsInstance(polinom, str)


class GeneratorTest(TestCase):
    def test_default_arguments(self):
        for generator in Problem.__subclasses__():
            for field in generator._meta.get_fields():
                if field.name not in [
                    "id",
                    "document",
                    "content_type",
                    "text",
                    "problem_ptr",
                ]:
                    self.assertNotEqual(
                        field.default,
                        NOT_PROVIDED,
                        f"{generator.__name__}, {field.name}",
                    )

    def test_default_text(self):
        for generator in Problem.__subclasses__():
            self.assertIsNotNone(generator.default_instruction)
            self.assertIsNotNone(generator.default_solution)
