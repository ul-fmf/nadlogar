import random

import sympy
from django.db import models

from .linearna import seznam_polovick, seznam_tretinj, skozi_tocki
from .meta import GeneratedDataIncorrect, Problem


def nicelna_oblika(od=-5, do=5, risanje=False):
    """
    Vrne naključno kvadratno funkcijo v ničelni obliki.
    :param od: najmanjša možna vrednost za ničlo funkcije
    :param do: največja možna vrednost za ničlo funkcije
    :param risanje: če fukcijo potrebujejmo za risanje, izbere lepši vodilni koeficient
    :return: vodilni koeficient, ničli in kvadratno funkcijo v ničelni obliki
    >>> nicelna_oblika(od=0, do=15)
    (-11/3, 7, 10/3, -11*(x - 7)*(x - 10/3)/3)
    >>> nicelna_oblika(od=-2, risanje=True)
    (2, -2, 3/2, 2*(x - 3/2)*(x + 2))
    """
    if risanje:
        a = random.choice([-2, -1, sympy.Rational(-1, 2), sympy.Rational(1, 2), 1, 2])
    else:
        a = random.choice(seznam_polovick(-4, 4) + seznam_tretinj(-4, 4))
    x1 = random.choice(seznam_polovick(od, do) + seznam_tretinj(od, do))
    x2 = random.choice(seznam_polovick(od, do) + seznam_tretinj(od, do))
    x = sympy.symbols("x")
    nicelna = sympy.Mul(a, x - x1, x - x2, evaluate=False)
    return (a, x1, x2, nicelna)


def splosna_oblika(risanje=False):
    """
    Vrne naključno kvadratno funkcijo v splošni obliki.
    :param risanje: če fukcijo potrebujejmo za risanje, izbere lepši vodilni koeficient
    :return: vrne seznam koeficientov in kvadratno funkcijo v splošni obliki
    >>> splosna_oblika()
    (8/3, 1/2, -1/3, 8*x**2/3 + x/2 - 1/3)
    >>> splosna_oblika(risanje=True)
    (-2, 5/2, 1/3, -2*x**2 + 5*x/2 + 1/3)
    """
    if risanje:
        a = random.choice([-2, -1, sympy.Rational(-1, 2), sympy.Rational(1, 2), 1, 2])
    else:
        a = random.choice(seznam_polovick(-4, 4) + seznam_tretinj(-4, 4))

    b = random.choice(seznam_polovick(-4, 4) + seznam_tretinj(-4, 4))
    c = random.choice(seznam_polovick(-4, 4) + seznam_tretinj(-4, 4))
    x = sympy.symbols("x")
    splosna = a * x**2 + b * x + c
    return (a, b, c, splosna)


def nicle(a, b, c):
    """
    Iz podanih koeficientov kvadratne funkcije izračuna ničli funkcije.
    :param a: vodilni koeficient
    :param b: linearni koeficient
    :param c: prosti člen
    :return: tuple ničel kvadratne funkcije
    >>> nicle(1,-4,4)
    (2, 2)
    >>> nicle(2,3,4)
    (-3/4 + sqrt(23)*I/4, -3/4 - sqrt(23)*I/4)
    """
    D = diskriminanta(a, b, c)
    if D >= 0:
        d = sympy.sqrt(D)
    else:
        d = sympy.sqrt(-D) * sympy.I
    x1 = (-b + d) / (2 * a)
    x2 = (-b - d) / (2 * a)
    return (x1, x2)


def izracunaj_teme(a, b, c):
    """
    Iz podanih koeficientov kvadratne funkcije koordinati temena.
    :param a: vodilni koeficient
    :param b: linearni koeficient
    :param c: prosti člen
    :return: tuple koordinat temena kvadratne funkcije
    >>> izracunaj_teme(2,-2,-12)
    (0.5, -12.5)
    >>> izracunaj_teme(2,1,-3)
    (-0.25, -3.125)
    """
    p = -b / (2 * a)
    q = -(diskriminanta(a, b, c)) / (4 * a)
    return (p, q)


def diskriminanta(a, b, c):
    """
    Iz podanih koeficientov kvadratne funkcije izračuna diskriminanto.

    :param a: vodilni koeficient
    :param b: linearni koeficient
    :param c: prosti člen
    :return: vrednost diskriminante kvadratne funkcije
    >>> diskriminanta(2,1,-3)
    25
    >>> diskriminanta(2,3,4)
    -23
    """
    return b**2 - 4 * a * c


class KvadratnaIzracunajNicle(Problem):
    """
    Naloga za računanje ničel kvadratne funkcije.
    """

    default_instruction = r"""Izračunaj ničli kvadratne funkcije $f(x)=@splosna$."""
    default_solution = r"""$x_1=(@x1)$, $x_2=(@x2)$"""

    kompleksni_nicli = models.BooleanField(
        "Kompleksni ničli",
        help_text="Ali sta ničli lahko kompleksni?",
        choices=[(True, "Da"), (False, "Ne")],
        default=False,
    )

    class Meta:
        verbose_name = "Kvadratna funkcija / Ničle kvadratne funkcije"

    def generate(self):
        (a, b, c, splosna) = splosna_oblika()
        if not self.kompleksni_nicli:
            if not (diskriminanta(a, b, c) >= 0 and abs(diskriminanta(a, b, c)) <= 200):
                raise GeneratedDataIncorrect
        else:
            if not (diskriminanta(a, b, c) < 0 and abs(diskriminanta(a, b, c)) <= 200):
                raise GeneratedDataIncorrect
        [x1, x2] = nicle(a, b, c)
        return {
            "splosna": sympy.latex(splosna),
            "x1": sympy.latex(x1),
            "x2": sympy.latex(x2),
        }


# class NarisiGraf(Problem):
#     """
#     Naloga za risanje grafa kvadratne funkcije.
#     """

#     default_instruction = r"Nariši graf funkcije $f(x)=@funkcija$"
#     default_solution = r"""$f(x)=@funkcija$\par
#     \begin{minipage}{\linewidth}
#     \centering
#     \begin{tikzpicture}[baseline]
#     \begin{axis}[axis lines=middle, xlabel=$x$, ylabel=$y$,
#     xtick={-5,-4,...,5}, ytick={-5,-4,...,5},
#     xmin=-5.5, xmax=5.5, ymin=-5.5, ymax=5.5,
#     extra x ticks={ @x1,@x2,@p },
#     extra y ticks={ @q,@zacetna },
#     extra x tick labels={ $(@x1)$,$(@x2)$,$(@p)$ },
#     extra y tick labels={ $(@q)$,$(@zacetna)$ },
#     extra x tick style={xticklabel style={above},},
#     extra y tick style={yticklabel style={right},},]
#     \addplot[domain =-5:5, color=black, smooth]{ @narisiFunkcijo };
#     \end{axis}
#     \end{tikzpicture}
#     \end{minipage}
#      """

#     class Meta:
#         verbose_name = "Kvadratna funkcija / Graf kvadratne funkcije"

#     def generate(self):
#         x = sympy.symbols("x")
#         (a, x1, x2, nicelna) = nicelna_oblika(-3, 3, risanje=True)
#         funkcija = sympy.expand(nicelna)
#         [p, q] = izracunaj_teme(a, -a * (x1 + x2), a * x1 * x2)
#         if not (abs(q) <= 5):
#             raise GeneratedDataIncorrect
#         zacetna = funkcija.subs(x, 0)
#         return {
#             "funkcija": sympy.latex(funkcija),
#             "narisiFunkcijo": nicelna,
#             "p": p,
#             "q": q,
#             "x1": x1,
#             "x2": x2,
#             "zacetna": zacetna,
#         }


class TemenskaOblika(Problem):
    """
    Naloga za dopoljevanje do popolnega kvadrata.
    """

    default_instruction = r"Zapiši temensko obliko funkcije $f(x)=@splosna$."
    default_solution = r"$f=@splosna$"

    class Meta:
        verbose_name = "Kvadratna funkcija / Temenska oblika kvadratne funkcije"

    def generate(self):
        (a, b, c, splosna) = splosna_oblika()
        D = diskriminanta(a, b, c)
        if not (D >= 0 and abs(D) <= 200):
            raise GeneratedDataIncorrect
        (p, q) = izracunaj_teme(a, b, c)
        return {"splosna": sympy.latex(splosna), "p": p, "q": q, "a": a}


class Presecisce(Problem):
    """
    Naloga za računanje presečišč parabole in premice.
    """

    default_instruction = (
        r"Izračunaj presečišče parabole $y=@parabola$ in premice $y=@premica$."
    )
    default_solution = r"$T_1(@x1,@y1)$, $T_2(@x2,@y2)$"

    class Meta:
        verbose_name = "Kvadratna funkcija / Presečišče parabole in premice"

    def generate(self):
        x = sympy.symbols("x")
        b = sympy.symbols("b")
        c = sympy.symbols("c")
        a = random.choice([-2, -1, sympy.Rational(-1, 2), sympy.Rational(1, 2), 1, 2])
        x1 = random.choice(seznam_polovick(-5, 5) + seznam_tretinj(-5, 5))
        x2 = random.choice(seznam_polovick(-5, 5) + seznam_tretinj(-5, 5))
        y1 = random.choice(seznam_polovick(-5, 5) + seznam_tretinj(-5, 5))
        y2 = random.choice(seznam_polovick(-5, 5) + seznam_tretinj(-5, 5))
        premica = skozi_tocki(x1, y1, x2, y2)[-1]
        koeficienta = sympy.solve(
            (a * x1**2 + b * x1 + c - y1, a * x2**2 + b * x2 + c - y2), b, c
        )
        if not (
            koeficienta != []
        ):  # Če ni rešitve vrne prazen seznam in ne praznega slovarja
            raise GeneratedDataIncorrect
        if not (abs(koeficienta[b]) < 5 and abs(koeficienta[c]) < 5):
            raise GeneratedDataIncorrect
        if not (abs(koeficienta[b]).q < 5 and abs(koeficienta[c]).q < 5):
            raise GeneratedDataIncorrect
        kvadratna = a * x**2 + koeficienta[b] * x + koeficienta[c]
        return {
            "parabola": sympy.latex(kvadratna),
            "premica": sympy.latex(premica),
            "x1": sympy.latex(x1),
            "x2": sympy.latex(x2),
            "y1": sympy.latex(y1),
            "y2": sympy.latex(y2),
        }


class KvadratnaNeenacba(Problem):
    """
    Naloga za reševanje kvadratne neenačbe.
    """

    default_instruction = r"Reši kvadratno neenačbo $@neenakost$."
    default_solution = r"$x \in @resitev$"

    primerjava_s_stevilom = models.BooleanField(
        "konstanta",
        help_text="Ali naj na le na eni strani enačbe nastopa kvadratna funkcija?",
        choices=[(True, "Da"), (False, "Ne")],
        default=True,
    )

    class Meta:
        verbose_name = "Kvadratna funkcija / Reševanje kvadratnih neenačb"

    def generate(self):
        x = sympy.symbols("x")
        splosna1 = splosna_oblika(risanje=True)[-1]
        if self.primerjava_s_stevilom:
            primerjava = random.choice(
                seznam_polovick(-10, 10) + seznam_tretinj(-10, 10)
            )
        else:
            primerjava = splosna_oblika()[-1]
        if not (splosna1 != primerjava):
            raise GeneratedDataIncorrect
        neenacaj = random.choice(["<", "<=", ">", ">="])
        neenakost = sympy.Rel(splosna1, primerjava, neenacaj)
        nicli = sympy.solve(sympy.Eq(splosna1, primerjava), x)
        if len(nicli) == 0:
            pass
        else:
            if not (
                nicli[0].is_real
                and abs(max(nicli, key=abs)) < 10
                and sympy.denom(max(nicli, key=sympy.denom)) < 20
            ):
                raise GeneratedDataIncorrect

        resitev = sympy.solveset(neenakost, domain=sympy.S.Reals)
        return {"neenakost": sympy.latex(neenakost), "resitev": sympy.latex(resitev)}


class SkoziTocke(Problem):
    """
    Naloga za določanje predpisa kvadratne funkcije iz treh točk, skozi katere poteka graf funkcije. Reševanje sistema treh enačb in treh neznank.
    """

    default_instruction = r"""Graf kvadratne funkcije $f$ poteka skozi točke $A(@x1,@y1)$, $B(@x2,@y2)$ in $C(@x3,@y3)$. Določi predpis funkcije $f$."""
    default_solution = r"$f(x)=@funkcija$"

    presecisca = models.BooleanField(
        "Presečišče z osema",
        help_text="Ali naj bosta podani presečišči s koordinatnima osema?",
        choices=[(True, "Da"), (False, "Ne (podane bodo tri naključne točke)")],
        default=True,
    )

    class Meta:
        verbose_name = "Kvadratna funkcija / Predpis kvadratne funkcije iz točk"

    def generate(self):
        x = sympy.symbols("x")
        (a, nicla1, nicla2, funkcija) = nicelna_oblika(risanje=True)
        if self.presecisca:
            x1 = nicla1
            x2 = 0
        else:
            x1 = random.randint(-5, 5)
            x2 = random.randint(-5, 5)

        x3 = random.randint(-5, 5)
        if not (len({x1, x2, x3}) == 3):
            raise GeneratedDataIncorrect
        y1 = funkcija.subs(x, x1)
        y2 = funkcija.subs(x, x2)
        y3 = funkcija.subs(x, x3)

        return {
            "x1": sympy.latex(x1),
            "x2": sympy.latex(x2),
            "x3": sympy.latex(x3),
            "y1": sympy.latex(y1),
            "y2": sympy.latex(y2),
            "y3": sympy.latex(y3),
            "funkcija": sympy.latex(sympy.expand(funkcija)),
        }
