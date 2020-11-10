import datetime
from django.test import TestCase
from naloge.models import Naloga
from .models import Test


class TestTest(TestCase):
    def setUp(self):
        self.stevilo_testov = 10

    def test_stevilo_nadlog(self):
        for stevilo_nalog in range(self.stevilo_testov):
            test = Test.objects.create(
                naslov="Testni test", datum=datetime.date.today()
            )
            for _ in range(stevilo_nalog):
                Naloga.objects.create(test=test)
            self.assertEqual(stevilo_nalog, test.naloge.count())
            nadloge = test.ustvari_nadlogo()
            self.assertEqual(stevilo_nalog, len(nadloge))
