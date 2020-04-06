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
        primeri = []
        for naloga in self.naloge.all():
            primeri.append((naloga.ustvari_primer(), naloga))
        return primeri
