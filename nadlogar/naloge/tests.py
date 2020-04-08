import datetime
from django.test import TestCase
from testi.models import Test
from .models import Naloga

class NalogaTest(TestCase):
    def setUp(self):
        self.test = Test.objects.create(
            naslov="Testni test",
            datum=datetime.date.today(),
        )
        self.stevilo_preizkusov = 100

    def test_krajsanje_ulomkov(self):
        """Naloga za krajšanje ulomkov vrne ustrezen slovar"""
        naloga = Naloga.objects.create(
            test=self.test,
            generator=Naloga.KRAJSANJE_ULOMKOV,
            zahtevnost=1,
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
        naloga = Naloga.objects.create(
            test=self.test,
            generator=Naloga.ISKANJE_NICEL_POLINOMA,
            zahtevnost=1,
        )
        for _ in range(self.stevilo_preizkusov):
            primer = naloga.ustvari_primer()
            nicle = primer.pop('nicle')
            polinom = primer.pop('polinom')
            self.assertEqual(primer, {})
            self.assertIsInstance(nicle, list)
            self.assertIsInstance(polinom, str)
