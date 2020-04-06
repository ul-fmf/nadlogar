import random
from django.db import models


class Naloga(models.Model):
    KRAJSANJE_ULOMKOV = 'UL'
    ISKANJE_NICEL_POLINOMA = 'PO'
    GENERATOR = [
        (KRAJSANJE_ULOMKOV, 'krajšanje ulomkov'),
        (ISKANJE_NICEL_POLINOMA, 'iskanje ničel polinoma'),
    ]
    test = models.ForeignKey('testi.Test', on_delete=models.CASCADE)
    generator = models.CharField(
        max_length=2,
        choices=GENERATOR,
    )
    zahtevnost = models.PositiveSmallIntegerField()

    class Meta:
        default_related_name = 'naloge'
        verbose_name_plural = 'naloge'

    def __str__(self):
        return f'{self.test}: {self.get_generator_display()}, zahtevnost: {self.zahtevnost}'

    def ustvari_primer(self):
        if self.generator == self.KRAJSANJE_ULOMKOV:
            faktor = random.randint(1, self.zahtevnost)
            return {
                'okrajsan_stevec': 1,
                'okrajsan_imenovalec': 3,
                'neokrajsan_stevec': faktor,
                'neokrajsan_imenovalec': 3 * faktor,
            }
        elif self.generator == self.ISKANJE_NICEL_POLINOMA:
            nicla = random.randint(1, self.zahtevnost)
            return {
                'nicle': [-nicla, nicla],
                'polinom': f'x^2 - {nicla ** 2}',
            }
        else:
            assert False

    def ime_predloge(self):
        ime = {
            self.ISKANJE_NICEL_POLINOMA: 'iskanje_nicel_polinoma',
            self.KRAJSANJE_ULOMKOV: 'krajsanje_ulomkov',
        }[self.generator]
        return f'naloge/primeri/{ime}.html'
