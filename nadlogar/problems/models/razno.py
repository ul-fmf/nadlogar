from .meta import *


class ProstoBesedilo(Problem):
    """Problem s poljubnim fiksnim vprašanjem in odgovorom, namenjen ročno sestavljenim nalogam."""

    vprasanje = models.TextField(
        "vprašanje", help_text="Poljubno besedilo vprašanja.", default=""
    )
    odgovor = models.TextField(
        "odgovor", help_text="Poljubno besedilo odgovora.", default=""
    )

    class Meta:
        verbose_name = "prosto besedilo"

    def generate(self):
        return {
            "vprasanje": self.vprasanje,
            "odgovor": self.odgovor,
        }


class KrajsanjeUlomkov(Problem):
    """Problem, v katerem je treba okrajšati dani ulomek."""

    najvecji_stevec = models.PositiveSmallIntegerField(
        "največji števec",
        help_text="Največji števec, ki se bo pojavljal v okrajšanem ulomku.",
        default=20,
    )
    najvecji_imenovalec = models.PositiveSmallIntegerField(
        "največji imenovalec",
        help_text="Največji imenovalec, ki se bo pojavljal v okrajšanem ulomku.",
        default=20,
    )
    najvecji_faktor = models.PositiveSmallIntegerField(
        "največji faktor",
        help_text="Največji faktor med neokrajšanim in okrajšanim ulomkom.",
        default=20,
    )

    class Meta:
        verbose_name = "krajšanje ulomkov"

    def generate(self):
        stevec = random.randint(1, self.najvecji_stevec)
        imenovalec = random.randint(1, self.najvecji_imenovalec)
        faktor = random.randint(1, self.najvecji_faktor)
        return {
            "okrajsan_stevec": stevec,
            "okrajsan_imenovalec": imenovalec,
            "neokrajsan_stevec": faktor * stevec,
            "neokrajsan_imenovalec": faktor * imenovalec,
        }


class IskanjeNicelPolinoma(Problem):
    """Problem, v katerem je treba poiskati ničle danega polinoma."""

    stevilo_nicel = models.PositiveSmallIntegerField(
        "število ničel",
        help_text="Največje število ničel polinoma (vedno bo vsaj 1).",
        default=3,
    )
    velikost_nicle = models.PositiveSmallIntegerField(
        "velikost ničle",
        help_text="Največja velikost ničle glede na absolutno vrednost.",
        default=9,
    )

    class Meta:
        verbose_name = "iskanje ničel polinoma"

    def generate(self):
        nicla = random.randint(1, self.velikost_nicle)
        if self.stevilo_nicel % 2 == 0:
            nicle = {nicla, -nicla}
        else:
            nicle = {nicla}
        polinom = f"x^{self.stevilo_nicel} - {nicla ** self.stevilo_nicel}"
        return {"nicle": nicle, "polinom": polinom}
