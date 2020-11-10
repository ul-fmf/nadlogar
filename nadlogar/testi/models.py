from django.db import models


class Test(models.Model):
    naslov = models.CharField(max_length=255)
    datum = models.DateField()
    opis = models.TextField(blank=True)

    class Meta:
        ordering = ['datum', 'naslov']
        verbose_name_plural = 'testi'

    def __str__(self):
        return f'{self.naslov} ({self.datum})'

    def ustvari_nadlogo(self):
        return [naloga.doloci_tip().ustvari_primer_in_besedilo() for naloga in self.naloge.all()]
