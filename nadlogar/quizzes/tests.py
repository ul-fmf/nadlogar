import datetime

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from problems.models import KrajsanjeUlomkov, ProblemText
from students.models import Student, StudentGroup

from .models import Quiz


class QuizTest(TestCase):
    def setUp(self):
        self.stevilo_testov = 10
        self.stevilo_studentov = 5
        self.student_group = StudentGroup.objects.create(name="Testna skupina")
        self.students = [
            Student.objects.create(
                name="Študent {}".format(i), group=self.student_group
            )
            for i in range(self.stevilo_studentov)
        ]

    def test_stevilo_nadlog(self):
        for stevilo_nalog in range(self.stevilo_testov):
            quiz = Quiz.objects.create(
                name="Testni kviz",
                date=datetime.date.today(),
                student_group=self.student_group,
            )
            problem_text = ProblemText.objects.create(
                content_type=ContentType.objects.get_for_model(KrajsanjeUlomkov)
            )
            for _ in range(stevilo_nalog):
                KrajsanjeUlomkov.objects.create(
                    quiz=quiz,
                    text=problem_text,
                    najvecji_stevec=10,
                    najvecji_imenovalec=10,
                    najvecji_faktor=10,
                )
            self.assertEqual(stevilo_nalog, quiz.problems.count())
            nadloge = quiz.generate_everything()
            self.assertEqual(self.stevilo_studentov, len(nadloge))
            for nadloge_studenta in nadloge.values():
                self.assertEqual(stevilo_nalog, len(nadloge_studenta))
