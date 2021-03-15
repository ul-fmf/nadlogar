import datetime

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from quizzes.models import Quiz
from students.models import StudentGroup

from . import models


class ProblemTest(TestCase):
    def setUp(self):
        self.student_group = StudentGroup.objects.create(name="Testna skupina")
        self.quiz = Quiz.objects.create(
            name="Testni kviz",
            date=datetime.date.today(),
            student_group=self.student_group,
        )
        self.stevilo_preizkusov = 100

    def test_krajsanje_ulomkov(self):
        """Generator za krajšanje ulomkov vrne ustrezen slovar"""
        problem_text = models.ProblemText.objects.create(
            content_type=ContentType.objects.get_for_model(models.KrajsanjeUlomkov)
        )
        problem = models.KrajsanjeUlomkov.objects.create(
            quiz=self.quiz,
            text=problem_text,
            najvecji_stevec=1,
            najvecji_imenovalec=1,
            najvecji_faktor=1,
        )
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
        problem_text = models.ProblemText.objects.create(
            content_type=ContentType.objects.get_for_model(models.IskanjeNicelPolinoma)
        )
        problem = models.IskanjeNicelPolinoma.objects.create(
            quiz=self.quiz,
            text=problem_text,
            stevilo_nicel=3,
            velikost_nicle=20,
        )
        for seed in range(self.stevilo_preizkusov):
            primer = problem.generate_data(seed)
            nicle = primer.pop("nicle")
            polinom = primer.pop("polinom")
            self.assertEqual(primer, {})
            self.assertIsInstance(nicle, set)
            self.assertIsInstance(polinom, str)
