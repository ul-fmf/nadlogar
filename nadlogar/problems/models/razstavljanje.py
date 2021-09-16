from .meta import *


class RazstaviVieta(Problem):
    """Problem za razstavljanje s pomočjo Vietovega pravila."""

    maksimalna_vrednost = models.PositiveSmallIntegerField(
        "maksimalna vrednost",
        help_text="Največja možna vrednost razstavljenega člena glede na absolutno vrednost",
        default=15,
    )
    vodilni_koeficient = models.BooleanField(
        "vodilni koeficient",
        help_text="Ali naj bo vodilni koeficient različen od 1?",
        default=True,
    )

    class Meta:
        verbose_name = "razstavi Vieta"

    def generate(self):
        x1 = random.randint(-self.maksimalna_vrednost, self.maksimalna_vrednost)
        x2 = random.randint(-self.maksimalna_vrednost, self.maksimalna_vrednost)
        a = (
            random.choice([1, -1]) * random.randint(2, 4)
            if self.vodilni_koeficient
            else 1
        )

        x = sympy.symbols("x")
        razstavljen = sympy.Mul(a, (x - x1), (x - x2), evaluate=False).simplify()
        izraz = razstavljen.expand()

        return {"izraz": sympy.latex(izraz), "razstavljen": sympy.latex(razstavljen)}


class RazstaviRazliko(Problem):
    """Problem za razstavljanje razlike kvadratov, kubov in višjih potenc."""

    najmanjsa_potenca = models.PositiveSmallIntegerField(
        "najmanjša potenca",
        help_text="Najmanjša možna potenca za razstavljanje.",
        default=2,
    )
    najvecja_potenca = models.PositiveSmallIntegerField(
        "največja potenca",
        help_text="Največja možna potenca za razstavljanje.",
        default=4,
    )
    linearna_kombinacija = models.BooleanField(
        "linearna kombinacija",
        help_text="Ali naj naloga vsebuje linearno kombinacijo dveh neznank ali enostaven dvočlenik?",
        default=True,
    )

    class Meta:
        verbose_name = "razstavi razliko"

    def generate(self):
        if self.najmanjsa_potenca > self.najvecja_potenca:
            self.najmanjsa_potenca, self.najvecja_potenca = (
                self.najvecja_potenca,
                self.najmanjsa_potenca,
            )

        potenca = random.randint(self.najmanjsa_potenca, self.najvecja_potenca)
        if potenca == 2:
            do = 10
        else:
            do = 5
        simboli = ["a", "b", "c", "x", "y", "z", "v", "t"]
        izbran_simbol = random.choice(simboli)
        x = sympy.symbols(izbran_simbol)
        simboli.remove(izbran_simbol)
        if not self.linearna_kombinacija:
            a = 1
            b = random.choice([x for x in range(-do, do) if x != 0])
            y = 1
            m = 1
            n = 1
        else:
            a = random.randint(1, do)
            b = random.choice([x for x in range(-do, do) if x != 0])
            n = random.randint(1, 3)
            m = random.randint(1, 3)
            y = sympy.symbols(random.choice(simboli))
        izraz = (a * x ** n) ** potenca - (b * y ** m) ** potenca
        razstavljen = sympy.factor(izraz)

        return {"izraz": sympy.latex(izraz), "razstavljen": sympy.latex(razstavljen)}
