import datetime
from django.test import TestCase
from testi.models import Test
from . import models

class NalogaTest(TestCase):
    def setUp(self):
        self.test = Test.objects.create(
            naslov="Testni test",
            datum=datetime.date.today(),
        )
        self.stevilo_preizkusov = 100

    def test_krajsanje_ulomkov(self):
        """Naloga za krajšanje ulomkov vrne ustrezen slovar"""
        naloga = models.KrajsanjeUlomkov.objects.create(
            test=self.test,
            najvecji_stevec=1,
            najvecji_imenovalec=1,
            najvecji_faktor=1,
        )
        for _ in range(self.stevilo_preizkusov):
            primer = naloga.ustvari_primer()
            a = primer.pop('okrajsan_stevec')
            b = primer.pop('okrajsan_imenovalec')
            c = primer.pop('neokrajsan_stevec')
            d = primer.pop('neokrajsan_imenovalec')
            self.assertEqual(primer, {})
            self.assertEqual(a * d, b * c)

    def test_iskanje_nicel_polinoma(self):
        """Naloga za iskanje ničel polinoma vrne ustrezen slovar"""
        naloga = models.IskanjeNicelPolinoma.objects.create(
            test=self.test,
            stevilo_nicel=3,
            velikost_nicle=20,
        )
        for _ in range(self.stevilo_preizkusov):
            primer = naloga.ustvari_primer()
            nicle = primer.pop('nicle')
            polinom = primer.pop('polinom')
            self.assertEqual(primer, {})
            self.assertIsInstance(nicle, set)
            self.assertIsInstance(polinom, str)
