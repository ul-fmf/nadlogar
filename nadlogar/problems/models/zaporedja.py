import random

import sympy
from django.db import models

from .meta import Problem


class SplosniClenZaporedja(Problem):
    """Naloga za iskanje splošnega člena poljubnega zaporedja."""

    default_instruction = r"Poišči predpis za splošni člen, ki mu zadoščajo začetni členi zaporedja $@cleni, \ldots$"
    default_solution = r"$a_n = @resitev$"

    zamik_alternirajoce = models.BooleanField(
        "zamaknjeno in alternirajoče zaporedje",
        help_text="So v izbor predpisa vljučena zamaknjena zaporedja iz kvadratov in  kubov ter alternirajoča zaporedja?",
        choices=[(True, "Da"), (False, "Ne")],
        default=False,
    )

    class Meta:
        verbose_name = "Zaporedja / splošni člen zaporedja"

    def generate(self):
        n = sympy.symbols("n")
        a = random.choice([x for x in range(-5, 5) if x != 0])
        b = random.choice([x for x in range(-3, 3) if x != 0])
        c = random.choice([x for x in range(1, 3) if x != 0])
        d = random.choice([x for x in range(1, 3) if x != 0])
        predpisi = [
            a + (n - 1) * b,
            a * b ** (n - 1),
            sympy.Mul(
                (a + b * (n - 1)),
                sympy.Pow(c + d * (n - 1), -1, evaluate=False),
                evaluate=False,
            ),
            n**2,
            n**3,
        ]
        if self.zamik_alternirajoce:
            predpisi += [
                n**2 - a,
                n**3 - a,
                (-1) ** n * a * b ** (n - 1),
            ]
        predpis = random.choice(predpisi)
        cleni = []
        for x in range(1, 6):
            cleni.append(predpis.subs(n, x))
        return {
            "cleni": ", ".join([sympy.latex(c) for c in cleni]),
            "resitev": sympy.latex(predpis),
        }
