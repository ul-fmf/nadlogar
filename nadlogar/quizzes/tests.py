import datetime

from django.test import TestCase
from problems.models import KrajsanjeUlomkov

from .models import Quiz


class QuizTest(TestCase):
    def setUp(self):
        self.stevilo_testov = 10

    def test_stevilo_nadlog(self):
        for stevilo_nalog in range(self.stevilo_testov):
            quiz = Quiz.objects.create(name="Testni kviz", date=datetime.date.today())
            for _ in range(stevilo_nalog):
                KrajsanjeUlomkov.objects.create(
                    quiz=quiz,
                    najvecji_stevec=10,
                    najvecji_imenovalec=10,
                    najvecji_faktor=10,
                )
            self.assertEqual(stevilo_nalog, quiz.problems.count())
            nadloge = quiz.generate_everything()
            self.assertEqual(stevilo_nalog, len(nadloge))
