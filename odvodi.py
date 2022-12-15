import random

import sympy
from django.db import models

from .meta import GeneratedDataIncorrect, Problem


def kot_med_premicama(k1, k2):
    """
    Izračuna kot med premicama iz smernih koeficientov (v radianih).
    """
    if k1 * k2 == -1:
        kot = sympy.pi / 2
    else:
        kot = sympy.atan(abs((k2 - k1) / (1 + k1 * k2)))
    return kot


def generiraj_polinom(min_stopnja=2, max_stopnja=3):
    """
    Vrne naključen polinom.
    >>> izberi_polinom(max_stopnja=5)
    -2*x**4 + x**3 + 2*x**2 + 2*x + 3
    """
    x = sympy.symbols("x")
    stopnja = random.randint(min_stopnja, max_stopnja)
    polinom = sympy.Poly(
        [random.choice([-2, -1, 1, 2])]
        + [random.randint(-3, 3) for i in range(stopnja)],
        x,
    ).as_expr()  # Pazi za stacionarne naj bo največ 3.stopnje!
    return polinom


def generiraj_racionalno(
    min_stopnja_stevca=2,
    max_stopnja_stevca=4,
    min_stopnja_imenovalca=1,
    max_stopnja_imenovalca=2,
):
    """
    Vrne naključno racionalno funkcijo.
    generiraj_racionalno(min_stopnja_stevca=3, min_stopnja_imenovalca=3, max_stopnja_imenovalca=3)
    (-2*x**3 + 3*x**2 - x + 1)/(x**3 + 3*x**2 - 3*x - 2)
    """
    x = sympy.symbols("x")
    stopnja_stevca = random.randint(min_stopnja_stevca, max_stopnja_stevca)
    stopnja_imenovalca = random.randint(min_stopnja_imenovalca, max_stopnja_imenovalca)
    stevec = sympy.Poly(
        [random.choice([-2, -1, 1, 2])]
        + [random.randint(-3, 3) for i in range(stopnja_stevca)],
        x,
    ).as_expr()
    imenovalec = sympy.Poly(
        [random.choice([-2, -1, 1, 2])]
        + [random.randint(-3, 3) for i in range(stopnja_imenovalca)],
        x,
    ).as_expr()
    racionalna = sympy.simplify(stevec / imenovalec)
    return racionalna


def generiraj_eksponentno(osnove=[sympy.E, 2, 3, 5]):
    """
    Vrne naključno eksponentno funkcijo z eno izmed podanih osnov.
    """
    x = sympy.symbols("x")
    osnova = random.choice(osnove)
    eksponentna = osnova**x
    return eksponentna


def izberi_logaritem(osnove=[sympy.E, 2, 3, 4, 5, 10]):
    """
    Vrne naključno logaritemsko funkcijo z eno izmed podanih osnov.
    Opomba: Program vse logaritme spremeni v logaritme z osnovo :math:`e` in naravni logaritem izpiše kot :math:`log(x)`.
    izberi_logaritem(osnove=[3,5])
    log(x)/log(5)
    """
    x = sympy.symbols("x")
    osnova = random.choice(osnove)
    logaritem = sympy.log(x, osnova)  # todo izpis log_baza v latexu
    # Todo latex naj namesto log izpiše ln, to lahko popravimo kar ročno z regex izrazom
    return logaritem


def izberi_nakljucno_kotno_funkcijo():
    """
    Vrne kosinus, sinus, tangens ali kotangens.
    """
    x = sympy.symbols("x")
    kosinus = sympy.cos(x)
    sinus = sympy.sin(x)
    tangens = sympy.tan(x)
    kotangens = sympy.cot(x)
    return random.choice([kosinus, sinus, tangens, kotangens])


def izberi_nakljucno_krozno_funkcijo():
    """
    Vrne arkus kosinus, arkus sinus, arkus tangens ali arkus kotangens.
    :return: krožno funkcijo
    >>> izberi_nakljucno_krozno_funkcijo()
    asin(x)
    >>> izberi_nakljucno_krozno_funkcijo()
    acot(x)
    """
    x = sympy.symbols("x")
    arcus_kosinus = sympy.acos(x)
    arcus_sinus = sympy.asin(x)
    arcus_tangens = sympy.atan(x)
    arcus_kotangens = sympy.acot(x)
    return random.choice([arcus_kosinus, arcus_sinus, arcus_tangens, arcus_kotangens])
