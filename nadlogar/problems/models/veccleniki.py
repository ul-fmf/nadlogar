from .meta import *


class PotencaDvoclenika(Problem):
    """Problem za potenciranje dvočlenika."""

    najmanjsa_potenca = models.PositiveSmallIntegerField(
        "najmanjša potenca",
        help_text="Najmanjša možna potenca dvočlenika.",
        default=2,
    )
    najvecja_potenca = models.PositiveSmallIntegerField(
        "največja potenca",
        help_text="Največja možna potenca dvočlenika.",
        default=4,
    )
    linearna_kombinacija = models.BooleanField(
        "linearna kombinacija",
        help_text="Ali naj naloga vsebuje linearno kombinacijo dveh neznank ali enostaven dvočlenik?",
        default=True,
    )

    class Meta:
        verbose_name = "potenciranje dvočlenika"

    def generate(self):
        potenca = random.randint(self.najmanjsa_potenca, self.najvecja_potenca)
        simboli = ["a", "b", "c", "x", "y", "z", "v", "t"]
        izbran_simbol = random.choice(simboli)
        x = sympy.symbols(izbran_simbol)
        simboli.remove(izbran_simbol)
        if not self.linearna_kombinacija:
            a = 1
            b = random.choice([x for x in range(-5, 5) if x != 0])
            n = 1
            y = 1
            m = 1
        else:
            a = random.randint(1, 5)
            b = random.choice([x for x in range(-5, 5) if x != 0])
            n = random.randint(2, 5)
            m = random.randint(1, 5)
            y = sympy.symbols(random.choice(simboli))

        izraz = sympy.Pow(a * x ** n + b * y ** m, potenca, evaluate=False)
        return {
            "izraz": sympy.latex(izraz),
            "resitev": sympy.latex(sympy.expand(izraz)),
        }


class PotencaTroclenika(Problem):
    """Problem za potenciranje tročlenika."""

    najmanjsa_potenca = models.PositiveSmallIntegerField(
        "najmanjša potenca",
        help_text="Najmanjša možna potenca tročlenika.",
        default=2,
    )
    najvecja_potenca = models.PositiveSmallIntegerField(
        "največja potenca",
        help_text="Največja možna potenca dvočlenika.",
        default=4,
    )
    linearna_kombinacija = models.BooleanField(
        "linearna kombinacija",
        help_text="Ali naj naloga vsebuje linearno kombinacijo treh neznank ali enostaven tročlenik?",
        default=True,
    )

    class Meta:
        verbose_name = "potenciranje tročlenika"

    def generate(self):
        potenca = random.randint(self.najmanjsa_potenca, self.najvecja_potenca)
        simboli = [sympy.symbols(x) for x in ["a", "b", "c", "x", "y", "z", "v", "t"]]
        x, y, z = random.sample(simboli, 3)
        a = random.randint(1, 4)
        b = random.choice([x for x in range(-4, 4) if x != 0])
        c = random.choice([x for x in range(-4, 4) if x != 0])
        if not self.linearna_kombinacija:
            a = 1
            b = 1
            z = 1

        izraz = sympy.Pow(a * x + b * y + c * z, potenca, evaluate=False)
        return {
            "izraz": sympy.latex(izraz),
            "resitev": sympy.latex(sympy.expand(izraz)),
        }


class PotencaVecclenika(Problem):
    """Problem za potenciranje veččlenika."""

    najmanjsa_potenca = models.PositiveSmallIntegerField(
        "najmanjša potenca",
        help_text="Najmanjša možna potenca veččlenika.",
        default=2,
    )
    najvecja_potenca = models.PositiveSmallIntegerField(
        "največja potenca",
        help_text="Največja možna potenca veččlenika.",
        default=4,
    )
    najmanj_clenov = models.PositiveSmallIntegerField(
        "najmanj členov",
        help_text="Najmanjše možno število členov v veččleniku.",
        default=2,
    )
    najvec_clenov = models.PositiveSmallIntegerField(
        "največ členov",
        help_text="Največje možno število členov v veččleniku.",
        default=4,
    )
    linearna_kombinacija = models.BooleanField(
        "linearna kombinacija",
        help_text="Ali naj naloga vsebuje linearno kombinacijo neznank ali enostaven veččlenik?",
        default=True,
    )

    class Meta:
        verbose_name = "potenciranje veččlenika"

    def generate(self):
        potenca = random.randint(self.najmanjsa_potenca, self.najvecja_potenca)
        cleni = random.randint(self.najmanj_clenov, self.najvec_clenov)
        simboli = [
            sympy.symbols(chr(x)) for x in random.sample(range(97, 123), cleni)
        ]  # izberemo naključne znake abecede
        if potenca == 2:
            do = 10
        else:
            do = 5

        koeficienti = random.choices([x for x in range(-do, do) if x != 0], k=cleni)
        if not self.linearna_kombinacija:
            potence = [1 for _ in range(cleni)]
        else:
            potence = random.choices(range(1, 4), k=cleni)

        vrednosti = zip(koeficienti, simboli, potence)
        izraz = sympy.Pow(
            sum(k * s ** p for k, s, p in vrednosti), potenca, evaluate=False
        )

        return {
            "izraz": sympy.latex(izraz),
            "resitev": sympy.latex(sympy.expand(izraz)),
        }
