from django.test import TestCase
from model_bakery import baker


class DocumentTest(TestCase):
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
            document = baker.make(
                "Document",
                student_group=self.student_group,
            )
            for _ in range(stevilo_nalog):
                baker.make(
                    "KrajsanjeUlomkov",
                    document=document,
                )
            self.assertEqual(stevilo_nalog, document.problems.count())
            nadloge = document.generate_student_problem_texts()
            self.assertEqual(self.stevilo_studentov, len(nadloge))
            for nadloge_studenta in nadloge.values():
                self.assertEqual(stevilo_nalog, len(nadloge_studenta))
