import random
from django.db import models
from django.contrib.contenttypes.models import ContentType


class Naloga(models.Model):
    test = models.ForeignKey('testi.Test', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    predloga_besedila_naloge = models.TextField(blank=True)
    predloga_besedila_resitve = models.TextField(blank=True)

    class Meta:
        default_related_name = 'naloge'
        verbose_name_plural = 'naloge'

    def __str__(self):
        return f'{self.test}: {self.content_type.name}'
    
    def save(self, *args, **kwargs):
        self.content_type = ContentType.objects.get_for_model(type(self))
        super().save(*args, **kwargs)

    def doloci_tip(self):
        content_type = self.content_type
        if content_type.model_class() == type(self):
            return self
        else:
            return content_type.get_object_for_this_type(naloga_ptr_id=self.id)

    privzeta_predloga_besedila_naloge = ''
    privzeta_predloga_besedila_resitve = ''

    def ustvari_primer(self):
        return {}
    
    def besedilo_naloge(self, primer):
        predloga = self.predloga_besedila_naloge or self.privzeta_predloga_besedila_naloge
        return predloga.format(**primer)

    def besedilo_resitve(self, primer):
        predloga = self.predloga_besedila_resitve or self.privzeta_predloga_besedila_resitve
        return predloga.format(**primer)
    
    def ustvari_primer_in_besedilo(self):
        primer = self.ustvari_primer()
        besedilo = self.besedilo_naloge(primer)
        resitev = self.besedilo_resitve(primer)
        return primer, besedilo, resitev


class KrajsanjeUlomkov(Naloga):
    najvecji_stevec = models.PositiveSmallIntegerField()
    najvecji_imenovalec = models.PositiveSmallIntegerField()
    najvecji_faktor = models.PositiveSmallIntegerField()

    def ustvari_primer(self):
        stevec = random.randint(1, self.najvecji_stevec)
        imenovalec = random.randint(1, self.najvecji_imenovalec)
        faktor = random.randint(1, self.najvecji_faktor)
        return {
            'okrajsan_stevec': stevec,
            'okrajsan_imenovalec': imenovalec,
            'neokrajsan_stevec': faktor * stevec,
            'neokrajsan_imenovalec': faktor * imenovalec,
        }

    privzeta_predloga_besedila_naloge = '''
        Okrajšaj ulomek $\\frac{{{neokrajsan_stevec}}}{{{neokrajsan_imenovalec}}}$.
    '''

    privzeta_predloga_besedila_resitve = '''
        $\\frac{{{okrajsan_stevec}}}{{{okrajsan_imenovalec}}}$
    '''


class IskanjeNicelPolinoma(Naloga):
    stevilo_nicel = models.PositiveSmallIntegerField()
    velikost_nicle = models.PositiveSmallIntegerField()

    def ustvari_primer(self):
        nicla = random.randint(1, self.velikost_nicle)
        if self.stevilo_nicel % 2 == 0:
            nicle = {nicla, -nicla}
        else:
            nicle = {nicla}
        polinom = f'x^{self.stevilo_nicel} - {nicla ** self.stevilo_nicel}'
        return {
            'nicle': nicle,
            'polinom': polinom
        }

    privzeta_predloga_besedila_naloge = '''
        Poišči vse ničle polonoma ${polinom}$.
    '''

    privzeta_predloga_besedila_resitve = '''
        ${nicle}$
    '''
