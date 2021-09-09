from .meta import *


class DeliteljVeckratnik(Problem):
    """Problem za izračun največjega skupnega delitelja in najmanjšega skupnega večkratnika danega števila."""

    minimalna_vrednost = models.PositiveSmallIntegerField(
        "minimalna vrednost",
        help_text="Najmanjša možna vrednost katerega izmed števil",
    )

    maksimalna_vrednost = models.PositiveSmallIntegerField(
        "maksimalna vrednost",
        help_text="Največja možna vrednost katerega izmed števil",
    )

    maksimalni_prafaktor = models.PositiveSmallIntegerField(
        "maksimalni prafaktor",
        help_text="Zgornja meja za prafaktorje števil",
    )

    class Meta:
        verbose_name = "največji skupni delitelj in najmanjši skupni večkratnik"

    def generate(self):
        stevilo1 = random.randint(self.minimalna_vrednost, self.maksimalna_vrednost)
        stevilo2 = random.randint(self.minimalna_vrednost, self.maksimalna_vrednost)
        if not (
            max(*sympy.factorint(stevilo1).keys(), *sympy.factorint(stevilo2).keys())
            <= self.maksimalni_prafaktor
            and stevilo1 != stevilo2
        ):
            raise GeneratedDataIncorrect
        najvecji_delitelj = sympy.gcd(stevilo1, stevilo2)
        najmanjsi_veckratnik = sympy.lcm(stevilo1, stevilo2)

        return {
            "stevilo1": stevilo1,
            "stevilo2": stevilo2,
            "najvecji_delitelj": najvecji_delitelj,
            "najmanjsi_veckratnik": najmanjsi_veckratnik,
        }
