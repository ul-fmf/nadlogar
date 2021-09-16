from django.db.models.fields import NOT_PROVIDED
from django.test import TestCase
from model_bakery import baker

from .models import Problem


class ProblemTest(TestCase):
    def setUp(self):
        self.stevilo_preizkusov = 100
        self.document = baker.make("Document")

    def test_krajsanje_ulomkov(self):
        """Generator za krajšanje ulomkov vrne ustrezen slovar"""
        # Don't forget to add document=self.document, otherwise model_bakery
        # will create a new document (and student group) for each problem.
        problem = baker.make("KrajsanjeUlomkov", document=self.document)
        for seed in range(self.stevilo_preizkusov):
            primer = problem.generate_data(seed)
            a = primer.pop("okrajsan_stevec")
            b = primer.pop("okrajsan_imenovalec")
            c = primer.pop("neokrajsan_stevec")
            d = primer.pop("neokrajsan_imenovalec")
            self.assertEqual(primer, {})
            self.assertEqual(a * d, b * c)

    def test_iskanje_nicel_polinoma(self):
        """Generator za iskanje ničel polinoma vrne ustrezen slovar"""
        # Don't forget to add document=self.document, otherwise model_bakery
        # will create a new document (and student group) for each problem.
        problem = baker.make("IskanjeNicelPolinoma", document=self.document)
        for seed in range(self.stevilo_preizkusov):
            primer = problem.generate_data(seed)
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
