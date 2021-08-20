from django.test import TestCase
from model_bakery import baker


class QuizTest(TestCase):
    def setUp(self):
        self.stevilo_testov = 10
        self.stevilo_studentov = 5
        self.student_group = baker.make("StudentGroup")
        self.students = [
            baker.make("Student", group=self.student_group)
            for i in range(self.stevilo_studentov)
        ]

    def test_stevilo_nadlog(self):
        for stevilo_nalog in range(self.stevilo_testov):
            quiz = baker.make(
                "Quiz",
                student_group=self.student_group,
            )
            for _ in range(stevilo_nalog):
                baker.make(
                    "KrajsanjeUlomkov",
                    quiz=quiz,
                )
            self.assertEqual(stevilo_nalog, quiz.problems.count())
            nadloge = quiz.generate_everything()
            self.assertEqual(self.stevilo_studentov, len(nadloge))
            for nadloge_studenta in nadloge.values():
                self.assertEqual(stevilo_nalog, len(nadloge_studenta))
