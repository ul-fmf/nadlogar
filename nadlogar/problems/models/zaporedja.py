import random

import sympy
from django.db import models

from .meta import Problem


def clen_aritmeticnega(a1, d, n):
    """
    Izračuna n-ti člen aritmetičnega zaporedja.
    :param a1: prvi člen aritmetičnega zaporedja
    :param d: diferenca aritmetičnega zaporedja
    :param n: zaporedni člen #TODO Ni člen ampak index člena?
    :return: n-ti člen aritmetičnega zaporedja
    >>> clen_aritmeticnega(1/2, 5, 17)
    80.5
    >>> clen_aritmeticnega(-10, 2, 50)
    88
    """
    an = a1 + (n - 1) * d
    return an


def niz_clenov(cleni, imena_clenov=False):
    """
    Vrne seznam členov zaporedja kot niz.
    :param cleni: seznam členov (sympy objekti)
    :param imena_clenov: ali člene zapiše v obliki a_i = ...
    """
    niz = r", ".join(
        (f"a_{i} = " if imena_clenov else "") + sympy.latex(c)
        for i, c in enumerate(cleni, 1)
    )
    return niz


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
            "cleni": niz_clenov(cleni),
            "resitev": sympy.latex(predpis),
        }


class PrviCleniAritmeticnega(Problem):
    """Naloga za zapis splošnega člena aritmetičnega zaporedja in računanje prvih petih členov, če poznaš prvi člen in diferenco."""

    default_instruction = r"""Zapiši prvih pet členov in splošni člen aritmetičnega zaporedja s prvim členom $a_1=@a1$
         in diferenco $d=@d$."""
    default_solution = r"""$@cleni, a_n=@splosni$"""

    class Meta:
        verbose_name = "Zaporedja / prvi člen aritmetičnega"

    racionalne_vrednosti = models.BooleanField(
        "prvi člen in diferenca zaporedja sta lahko racionalni vrednosti",
        help_text="",
        choices=[(True, "Da"), (False, "Ne")],
        default=False,
    )

    def generate(self):
        if not self.racionalne_vrednosti:
            a1 = random.choice([x for x in range(-12, 12) if x != 0])
            d = random.choice([x for x in range(-5, 5) if x != 0])
        else:
            a1 = random.choice(
                [sympy.Rational(1, x) for x in range(-6, 6) if x != 0]
                + [sympy.Rational(2, x) for x in range(-6, 6) if x != 0]
            )
            d = random.choice([sympy.Rational(1, x) for x in range(-6, 6) if x != 0])
        cleni = [a1]
        for N in range(2, 6):
            cleni.append(clen_aritmeticnega(a1, d, N))
        n = sympy.symbols("n")

        splosni = sympy.Add(a1, sympy.Mul(d, (n - 1), evaluate=False), evaluate=False)
        return {
            "cleni": niz_clenov(cleni, imena_clenov=True),
            "a1": sympy.latex(a1),
            "d": sympy.latex(d),
            "splosni": sympy.latex(splosni),
        }
