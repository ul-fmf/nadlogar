import random

import sympy
from django.db import models

from .meta import GeneratedDataIncorrect, Problem


def seznam_polovick(od=-10, do=10):
    """
    Funkcija sestavi seznam vseh celih iz polovic med vrednostima od in do (brez 0).
    :param od: najmanjša vrednost
    :param do: največja vrednost
    :return: seznam celih števil in polovic
    >>> seznam_polovick()
    [-10, -19/2, -9, -17/2, -8, -15/2, -7, -13/2, -6, -11/2, -5, -9/2, -4, -7/2, -3, -5/2, -2, -3/2, -1, -1/2, 1/2, 1, 3/2, 2, 5/2, 3, 7/2, 4, 9/2, 5, 11/2, 6, 13/2, 7, 15/2, 8, 17/2, 9, 19/2, 10, 21/2]
    >>> seznam_polovick(od=0, do=3)
    [1/2, 1, 3/2, 2, 5/2, 3, 7/2]
    """
    return [sympy.Rational(x, 2) for x in range(2 * od, 2 * (do + 1)) if x != 0]


def seznam_tretinj(od=-10, do=10):
    """
    Funkcija sestavi seznam vseh celih iz tretinj med vrednostima od in do (brez 0).
    :param od: najmanjša vrednost
    :param do: največja vrednost
    :return: seznam celih števil in tretinj
    >>> seznam_tretinj()
    [-10, -29/3, -28/3, -9, -26/3, -25/3, -8, -23/3, -22/3, -7, -20/3, -19/3, -6, -17/3, -16/3, -5, -14/3, -13/3, -4, -11/3, -10/3, -3, -8/3, -7/3, -2, -5/3, -4/3, -1, -2/3, -1/3, 1/3, 2/3, 1, 4/3, 5/3, 2, 7/3, 8/3, 3, 10/3, 11/3, 4, 13/3, 14/3, 5, 16/3, 17/3, 6, 19/3, 20/3, 7, 22/3, 23/3, 8, 25/3, 26/3, 9, 28/3, 29/3, 10, 31/3, 32/3]
    >>> seznam_tretinj(od=0, do=3)
    [1/3, 2/3, 1, 4/3, 5/3, 2, 7/3, 8/3, 3, 10/3, 11/3]
    """
    return [sympy.Rational(x, 3) for x in range(3 * od, 3 * (do + 1)) if x != 0]


def eksplicitna_premica():
    """
    Vrne naključno eksplicitno obliko premice, ki jo moramo izenačiti z y.
    :return: smerni koeficient, začetno vrednost in eksplicitno podano premico
    >>> eksplicitna_premica()
    (-4/3, 2, 2 - 4*x/3)
    >>> eksplicitna_premica()
    (3, -11/3, 3*x - 11/3)
    """
    # Funkcija vrne naključno eksplicitno podano premico
    k = random.choice(seznam_polovick(-3, 3) + seznam_tretinj(-3, 3))
    n = random.choice(seznam_polovick(-4, 4) + seznam_tretinj(-4, 4))
    x = sympy.symbols("x")
    eksplicitna = k * x + n
    return (k, n, eksplicitna)


def implicitna_premica():
    """
    Vrne implicitno podano obliko premice, ki jo moramo izenačiti z 0. Premice niso vzporedne z osema.
    :return: koeficiente in implicitno podano premico
    >>> implicitna_premica()
    (-7, 2, 3, -7*x + 2*y + 3)
    >>> implicitna_premica()
    (-2, 7, -6, -2*x + 7*y - 6)
    """
    seznamStevil = [x for x in range(-10, 10) if x != 0]
    a = random.choice(seznamStevil)
    b = random.choice(seznamStevil)
    c = random.choice(seznamStevil)
    x = sympy.symbols("x")
    y = sympy.symbols("y")
    implicitna = sympy.simplify(a * x + b * y + c)
    return (a, b, c, implicitna)


def skozi_tocki(x1, y1, x2, y2):
    """
    Izračuna predpis premice skozi dve točki.
    :param x1: x koordinata prve točke
    :param y1: y koordinata prve točke
    :param x2: x koordinata druge točke
    :param y2: y koordinata druge točke
    :return: smerni koeficient, začetno vrednost in eksplicitno podano premico
    >>> skozi_tocki(1,1,2,4)
    (3.0, -2.0, 3.0*x - 2.0)
    >>> skozi_tocki(-3,5,2,6)
    (0.2, 5.6, 0.2*x + 5.6)
    """
    x = sympy.symbols("x")
    k = (y2 - y1) / (x2 - x1)
    n = y1 - k * x1
    return (k, n, k * x + n)


def izberi_koordinato(od=-10, do=10):
    """
    Izbere poljubno celoštevilsko koordinato med vrednostima od in do.
    :param od: najmanjša vrednost
    :param do: največja vrednost
    :return: celoštevilsko koordinato
    >>> izberi_koordinato()
    2
    >>> izberi_koordinato(do=0)
    -4
    """
    koordinata = random.randint(od, do)
    return koordinata


def razdalja_med_tockama(x1, y1, x2, y2):
    """
    Izračuna razdaljo med dvema točkama.
    :param x1: abscisa prve točke
    :param y1: ordinata prve točke
    :param x2: abscisa druge točke
    :param y2: ordinata druge točke
    :return: razdaljo med točkama
    >>> razdalja_med_tockama(-14,6,-17,8)
    sqrt(13)
    >>> razdalja_med_tockama(2,-8,5,-12)
    5
    """

    razdalja = sympy.Point(x1, y1).distance(sympy.Point(x2, y2))
    return razdalja


class PremicaSkoziTocki(Problem):
    """
    Naloga za določanje enačbe premice skozi 2 točki.
    """

    default_instruction = (
        r"Zapiši enačbo premice skozi točki $A( @x1, @y1)$ in $B( @x2, @y2)$."
    )
    default_solution = r"$y=@premica$"

    class Meta:
        verbose_name = "Linearna funkcija / Enačba premice skozi dve točki"

    def generate(self):
        x1 = random.choice(seznam_polovick(-5, 5) + seznam_tretinj(-5, 5))
        y1 = random.choice(seznam_polovick(-5, 5) + seznam_tretinj(-5, 5))
        x2 = random.randint(-10, 10)
        y2 = random.randint(-10, 10)
        if not (
            x1 != x2 and y1 != y2
        ):  # Preveri, da sta 2 različni točki in nista vzporedni osem
            raise GeneratedDataIncorrect
        if not skozi_tocki(x1, y1, x2, y2)[0] in [
            sympy.Rational(x, y)
            for x in range(0, 6)
            for y in range(0, 2 * 10)
            if (x != 0 and y != 0)
        ]:  # Lepše rešitve
            raise GeneratedDataIncorrect
        premica = sympy.latex(skozi_tocki(x1, y1, x2, y2)[-1])
        return {
            "x1": sympy.latex(x1),
            "y1": sympy.latex(y1),
            "x2": sympy.latex(x2),
            "y2": sympy.latex(y2),
            "premica": premica,
        }


class RazdaljaMedTockama(Problem):
    """
    Naloga za računanje razdalje med dvema točkama v koordinatenm sistemu.
    """

    default_instruction = (
        r"Natančno izračunaj razdaljo med točkama $A (@x1,@y1)$ in $B (@x2,@y2)$."
    )
    default_solution = r"$d(A,B)=@razdalja$"

    class Meta:
        verbose_name = "Linearna funkcija / Računanje razdalje med dvema točkama"

    def generate(self):
        x1 = izberi_koordinato()
        y1 = izberi_koordinato()
        x2 = izberi_koordinato()
        y2 = izberi_koordinato()
        if not (x1 != x2 and y1 != y2):
            raise GeneratedDataIncorrect
        razdalja = sympy.latex(razdalja_med_tockama(x1, y1, x2, y2))
        return {
            "x1": sympy.latex(x1),
            "y1": sympy.latex(y1),
            "x2": sympy.latex(x2),
            "y2": sympy.latex(y2),
            "razdalja": razdalja,
        }


class OblikeEnacbPremice(Problem):
    """
    Naloga za pretvarjanje med različnimi oblikami enačbe premice.
    """

    default_instruction = (
        r"Zapiši eksplicitno in odsekovno obliko premice podane z enačbo $@implicitna$"
    )
    default_solution = r"$@eksplicitna$ in $@odsekovna$"

    class Meta:
        verbose_name = "Linearna funkcija / Odsekovna in eksplicitna oblika"

    def generate(self):
        x = sympy.symbols("x")
        y = sympy.symbols("y")
        (koeficient_x, koeficient_y, prosti, implicitnaOblika) = implicitna_premica()

        implicitna = sympy.latex(sympy.Eq(implicitnaOblika, 0))
        eksplicitna = sympy.latex(
            sympy.Eq(
                y,
                sympy.Rational(-koeficient_x, koeficient_y) * x
                + sympy.Rational(-prosti, koeficient_y),
                evaluate=False,
            )
        )
        odsekovna = sympy.latex(
            sympy.Eq(
                sympy.Rational(-koeficient_x, prosti) * x
                + sympy.Rational(-koeficient_y, prosti) * y,
                1,
            )
        )

        return {
            "implicitna": implicitna,
            "eksplicitna": eksplicitna,
            "odsekovna": odsekovna,
        }


class PremiceTrikotnik(Problem):
    """
    Naloga za računanje ploščine trikotnika, ki ga dve premici oklepata z abscisno osjo.
    """

    default_instruction = (
        r"Izračunaj ploščino trikotnika, ki ga premici $@premica1$ in $@premica2$"
        r" oklepata z abscisno osjo."
    )
    default_solution = r"$S=@ploscina$"

    class Meta:
        verbose_name = "Linearna funkcija / Ploščina trikotnika"

    def generate(self):
        x1 = izberi_koordinato(1, 5)
        y1 = 0
        x2 = random.choice([x for x in range(-5, 6) if x != 0])
        y2 = random.choice([x for x in range(-5, 6) if x != 0])
        x3 = izberi_koordinato(-5, 0)
        y3 = 0
        x = sympy.symbols("x")
        y = sympy.symbols("y")
        if not (x2 != x1 and x2 != x3):  # premici sta vzporedni
            raise GeneratedDataIncorrect
        if x2 == x1:
            premica1 = sympy.Eq(x, x1)
        else:
            k1 = sympy.Rational((y2 - y1), (x2 - x1))
            n1 = y1 - k1 * x1
            premica1 = sympy.Eq(y, k1 * x + n1)
        if x3 == x2:
            premica2 = sympy.Eq(x, x3)
        else:
            k2 = sympy.Rational((y3 - y2), (x3 - x2))
            n2 = y3 - k2 * x3
            premica2 = sympy.Eq(y, k2 * x + n2)

        ploscina_trikotnika = (
            sympy.latex(
                sympy.simplify(
                    abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2
                ).evalf(3)
            )
            .rstrip("0")
            .rstrip(".")
        )

        return {
            "premica1": sympy.latex(premica1),
            "premica2": sympy.latex(premica2),
            "ploscina": ploscina_trikotnika,
        }


# class NarisiLinearnoFunkcijo(Problem):
#     """
#     Naloga za risanje grafa linearne premice.
#     """

#     default_instruction = r"Nariši graf funkcije linearne $f(x) =  @linearna$."
#     default_solution = r"""$f(x)= @linearna$\par
#     \begin{minipage}{\linewidth}
#     \centering
#     \begin{tikzpicture}[baseline]
#     \begin{axis}[axis lines=middle, xlabel=$x$, ylabel=$y$,
#     xtick={-5,-4,...,5}, ytick={-5,-4,...,5},
#     xmin=-5.5, xmax=5.5, ymin=-5.5, ymax=5.5,
#     extra x ticks={ @nicla },
#     extra y ticks={ @n },
#     extra x tick labels={ $ @nicla$ },
#     extra y tick labels={ $ @n$},
#     extra x tick style={xticklabel style={above},},
#     extra y tick style={yticklabel style={right},},]
#     \addplot[domain =-5:5, color=black]{ @linearna };
#     \end{axis}
#     \end{tikzpicture}
#     \end{minipage}"""

#     class Meta:
#         verbose_name = "Linearna funkcija / Risanje grafa linearne funkcije"

#     def generate(self):
#         (k, n, eksplicitna) = eksplicitna_premica()
#         nicla = (-n) / k
#         return {
#             "linearna": sympy.latex(eksplicitna),
#             "n": sympy.latex(n),
#             "nicla": sympy.latex(nicla),
#         }


class VrednostiLinearne(Problem):
    """
    Naloga za računanje vrednosti x oziroma f(x) linearne funkcije. Potrebno določiti tudi kdaj je funkcija negativna.
    """

    default_instruction = (
        r"Dana je funkcija s predpisom $@linearna$. Izračunajte vrednost $f (@x1)$ in"
        r" za kateri $x$ je $f(x)=@y2$. Za katere vrednosti $x$ so vrednosti funkcije"
        r" negativne?"
    )
    default_solution = r"$f (@x1)=@y1$, $x=@x2$, $x \in @negativno$"

    class Meta:
        verbose_name = "Linearna funkcija / Vrednosti linearne funkcije"

    def generate(self):
        f = sympy.symbols("f(x)")

        (k, n, funkcija) = eksplicitna_premica()

        x1 = random.choice(seznam_polovick(-3, 3) + seznam_tretinj(-3, 3))
        x2 = random.choice(seznam_polovick(-3, 3) + seznam_tretinj(-3, 3))
        if not (x1 != x2):
            raise GeneratedDataIncorrect
        y1 = k * x1 + n
        y2 = k * x2 + n

        negativno = sympy.latex(sympy.solveset(funkcija < 0, domain=sympy.S.Reals))
        return {
            "linearna": sympy.latex(sympy.Eq(f, funkcija)),
            "x1": sympy.latex(x1),
            "x2": sympy.latex(x2),
            "y1": sympy.latex(y1),
            "y2": sympy.latex(y2),
            "negativno": negativno,
        }


class Neenacba(Problem):
    """
    Naloga za reševanje linearne neenačbe.
    """

    default_instruction = r"Reši neenačbo $ @neenacba$."
    default_solution = r"$x \in  @resitev$"

    kvadratna = models.BooleanField(
        "Kvadratna enačba",
        help_text="Ali naj bosta enačbi kvadratni?",
        choices=[(True, "Da (kvadratna člena se odštejeta)"), (False, "Ne")],
        default=False,
    )

    class Meta:
        verbose_name = "Linearna funkcija / Linearne neenačbe"

    def generate(self):
        x = sympy.symbols("x")
        izbor = [x for x in range(-5, 5) if x != 0]
        if not self.kvadratna:
            a = random.choice(izbor)
            b = random.choice(izbor)
            c = random.choice(izbor)
            d = random.choice(izbor)
            leva = a * x + b
            desna = c * x + d
        else:
            a = random.choice(izbor)
            x1 = random.choice(izbor)
            x2 = random.choice(izbor)
            x3 = random.choice(izbor)
            x4 = random.choice(izbor)
            leva = sympy.simplify(sympy.Mul(a, (x - x1), (x - x2), evaluate=False))
            desna = a * (x - x3) * (x - x4)

        neenacaj = random.choice(["<", "<=", ">", ">="])
        neenacba = sympy.Rel(leva, desna, neenacaj)
        resitev = sympy.solveset(sympy.expand(neenacba), x, domain=sympy.S.Reals)
        return {"neenacba": sympy.latex(neenacba), "resitev": sympy.latex(resitev)}


class SistemDvehEnacb(Problem):
    """
    Naloga za reševanje sistema dveh enačb z dvema nezankama.
    """

    default_instruction = r"Reši sistem enačb $ @enacba1$ in $ @enacba2$."
    default_solution = r"$x= @x$, $y= @y$"

    racionalno = models.BooleanField(
        "Racionalne rešitve",
        help_text="Ali smejo biti rešitve racionalne?",
        choices=[(True, "Da"), (False, "Ne (samo cela števila)")],
        default=False,
    )

    class Meta:
        verbose_name = "Linearna funkcija / Sistem dveh linearnih enačb"

    def generate(self):
        x = sympy.symbols("x")
        y = sympy.symbols("y")
        izborCela = [x for x in range(-5, 6) if x != 0]
        izborUlomki = (
            [sympy.Rational(x, 2) for x in [-3, -1, 1, 3]]
            + [sympy.Rational(x, 3) for x in [-2, -1, 1, 2]]
            + [sympy.Rational(x, 4) for x in [-3, -1, 1, 3]]
        )
        if not self.racionalno:
            x1 = random.choice(izborCela + [0])
            y1 = random.choice(izborCela + [0])
        else:
            x1 = random.choice(izborCela + izborUlomki + [0])
            y1 = random.choice(izborCela + izborUlomki + [0])
        a = random.choice(izborCela)
        b = random.choice(izborCela)
        d = random.choice(izborCela)
        e = random.choice(izborCela)
        if not ((a, b) != (d, e) and (x1 != 0 or y1 != 0)):
            raise GeneratedDataIncorrect
        c = a * x1 + b * y1
        f = d * x1 + e * y1
        enacba1 = a * x + b * y
        enacba2 = d * x + e * y
        return {
            "enacba1": sympy.latex(sympy.Eq(enacba1, c)),
            "enacba2": sympy.latex(sympy.Eq(enacba2, f)),
            "x": x1,
            "y": y1,
        }


class SistemTrehEnacb(Problem):
    """Naloga za reševanje sistema treh enačb s tremi neznankami."""

    default_instruction = r"Reši sistem enačb $ @enacba1$, $ @enacba2$ in $ @enacba3$."
    default_solution = r"$x= @x$, $y= @y$, $z= @z$"

    manjsi_koeficienti = models.BooleanField(
        "Manjša števila",
        help_text="Ali naj bodo koeficienti omejeni na manjša števila?",
        choices=[(True, "Da"), (False, "Ne")],
        default=True,
    )

    class Meta:
        verbose_name = "Linearna funkcija / Sistem treh linearnih enačb"

    def generate(self):
        x = sympy.symbols("x")
        y = sympy.symbols("y")
        z = sympy.symbols("z")
        if self.manjsi_koeficienti:
            izborCela = [-2, -1, 0, 1, 2]
        else:
            izborCela = list(range(-5, 6))

        # vrednosti spremenljivk
        x1 = random.choice(izborCela)
        y1 = random.choice(izborCela)
        z1 = random.choice(izborCela)

        # vrednosti koeficientov pred spremenljivkami
        koef_x1 = random.choice(izborCela)
        koef_y1 = random.choice(izborCela)
        koef_z1 = random.choice(izborCela)
        koef_x2 = random.choice(izborCela)
        koef_y2 = random.choice(izborCela)
        koef_z2 = random.choice(izborCela)
        koef_x3 = random.choice(izborCela)
        koef_y3 = random.choice(izborCela)
        koef_z3 = random.choice(izborCela)

        if not (
            len(
                {
                    (koef_x1, koef_y1, koef_z1),
                    (koef_x2, koef_y2, koef_z2),
                    (koef_x3, koef_y3, koef_z3),
                }
            )
            == 3
            and (x1 != 0 or y1 != 0 or z1 != 0)
        ):
            raise GeneratedDataIncorrect

        # vrednosti enačb in enačbe
        vrednost1 = koef_x1 * x1 + koef_y1 * y1 + koef_z1 * z1
        vrednost2 = koef_x2 * x1 + koef_y2 * y1 + koef_z2 * z1
        vrednost3 = koef_x3 * x1 + koef_y3 * y1 + koef_z3 * z1
        enacba1 = koef_x1 * x + koef_y1 * y + koef_z1 * z
        enacba2 = koef_x2 * x + koef_y2 * y + koef_z2 * z
        enacba3 = koef_x3 * x + koef_y3 * y + koef_z3 * z

        return {
            "enacba1": sympy.latex(sympy.Eq(enacba1, vrednost1)),
            "enacba2": sympy.latex(sympy.Eq(enacba2, vrednost2)),
            "enacba3": sympy.latex(sympy.Eq(enacba3, vrednost3)),
            "x": x1,
            "y": y1,
            "z": z1,
        }
