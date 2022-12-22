import random

import sympy
from django.db import models

from .meta import GeneratedDataIncorrect, Problem


def razdalja_med_tockama(x1, y1, x2, y2):
    """
    Izračuna razdaljo med dvema točkama.
    """

    razdalja = sympy.Point(x1, y1).distance(sympy.Point(x2, y2))
    return razdalja


class PreseciscaKroznic(Problem):
    """
    Naloga za iskanje presečišč dveh krožnic.
    """

    default_instruction = r"Določi medsebojno lego krožnic $\mathcal{K}_1:@kroznica1$ in $\mathcal{K}_2:@kroznica2$ ter določi presešišča, če obstajajo."
    default_solution = r"Sekata se v $@presek$."
    # "

    class Meta:
        verbose_name = "Stožnice / iskanje presečišča dveh krožnic"

    def generate(self):
        p1 = random.randint(-5, 5)
        q1 = random.randint(-5, 5)
        p2 = random.randint(-5, 5)
        q2 = random.randint(-5, 5)
        x0 = random.randint(-5, 5)
        y0 = random.randint(-5, 5)
        if (p1, q1) == (p2, q2):
            raise GeneratedDataIncorrect
        r1 = razdalja_med_tockama(x0, y0, p1, q1)
        r2 = razdalja_med_tockama(x0, y0, p2, q2)
        kroznica1 = sympy.Circle(sympy.Point(p1, q1), r1)
        kroznica2 = sympy.Circle(sympy.Point(p2, q2), r2)
        presek_kroznic = kroznica1.intersection(kroznica2)
        tocke_preseka = [(A.x, A.y) for A in presek_kroznic]
        if (x0, y0) not in tocke_preseka:
            raise GeneratedDataIncorrect
        latex_zapis_tock = ""
        for id, tocka in enumerate(tocke_preseka):
            latex_zapis_tock += f"T_{id + 1} = {sympy.latex(tocka)}, "
        latex_zapis_tock = latex_zapis_tock[:-2]
        izpis_kroznica1 = sympy.Eq(kroznica1.equation() + r1**2, r1**2)
        izpis_kroznica2 = sympy.Eq(kroznica2.equation() + r2**2, r2**2)
        return {
            "kroznica1": sympy.latex(izpis_kroznica1),
            "kroznica2": sympy.latex(izpis_kroznica2),
            "presek": latex_zapis_tock,
        }


# ~~~~~ Elipsa
class TemeGorisceEnacba(Problem):
    """
    Naloga za zapis predpisa elipse, če poznamo središče, teme in gorišče.
    """

    default_instruction = r"Zapiši enačbo elipse s središčem $@sredisce$, temenom $T_1@teme$ in goriščem $F_1@gorisce$."
    default_solution = r"$@elipsa$."

    class Meta:
        verbose_name = "Stožnice / iskanje predpisa elipse"

    premaknjena = models.BooleanField(
        "premaknjena elipsa",
        help_text="Ali je elipsa premaknjena iz izhodišča?",
        choices=[(True, "Da"), (False, "Ne")],
        default=False,
    )

    def generate(self):
        if self.premaknjena:
            sredisce_elipse = sympy.Point(random.randint(-5, 5), random.randint(-5, 5))
        else:
            sredisce_elipse = sympy.Point(0, 0)
        vodoravna_polos = random.randint(1, 5)
        navpicna_polos = random.randint(1, 5)
        if vodoravna_polos == navpicna_polos:
            raise GeneratedDataIncorrect
        teme = random.choice(
            [
                sredisce_elipse.translate(x=vodoravna_polos),
                sredisce_elipse.translate(x=-vodoravna_polos),
                sredisce_elipse.translate(y=navpicna_polos),
                sredisce_elipse.translate(y=-navpicna_polos),
            ]
        )
        elipsa = sympy.Ellipse(sredisce_elipse, vodoravna_polos, navpicna_polos)
        gorisce = random.choice(elipsa.foci)
        return {
            "teme": sympy.latex((teme.x, teme.y)),
            "gorisce": sympy.latex((gorisce.x, gorisce.y)),
            "sredisce": sympy.latex((sredisce_elipse.x, sredisce_elipse.y)),
            "elipsa": sympy.latex(sympy.Eq(elipsa.equation() + 1, 1)),
        }


# TODO Zaenkrat zakomentirano, ko bomo pogruntali kaj je z risanjem grafov bomo lahko nadaljevali

# class NarisiKrivuljo(Problem):
#     """
#     Naloga za dopolnjevanja do popolnih kvadratov ter risanje krožnice ali elipse.
#     """

#     default_instruction = r"""Nariši krivuljo ${{latex(naloga.razsirjena)}}$."""
#     default_solution = r"""
#     ${{latex(naloga.krivulja)}}$\par
#     \begin{minipage}{\linewidth}
#     \centering
#     \begin{tikzpicture}[baseline]
#     \begin{axis}[axis lines=middle, xlabel=$x$, ylabel=$y$,
#     xtick={-6,-5,-4,...,5,6}, ytick={-6,-5,-4,...,5,6},
#     xmin=-6.5, xmax=6.5, ymin=-6.5, ymax=6.5,,axis equal image]
#     \addplot[black,mark = x, mark size=2pt] coordinates {({{naloga.p}},{{naloga.q}})};
#     \draw (axis cs:{{naloga.p}},{{naloga.q}}) ellipse [x radius={{naloga.a}}, y radius = {{naloga.b}}];
#     \end{axis}
#     \end{tikzpicture}
#     \end{minipage}"""

#     class Meta:
#         verbose_name = "Stožnice / risanje krožnice in elipse"

#     def generate(self):
#         x = sympy.symbols("x")
#         y = sympy.symbols("y")
#         if self.premaknjena:
#             p = random.randint(-2, 2)
#             q = random.randint(-2, 2)
#         else:
#             p = 0
#             q = 0
#         izbor = []
#         if self.kroznica:
#             izbor.append("kroznica")
#         if self.elipsa:
#             izbor.append("elipsa")
#         izbrana = random.choice(izbor)
#         if izbrana == "kroznica":
#             a = random.randint(1, 4)
#             b = a
#             r = a  # definiran r zaradi različnega izpisa krivulj
#             krivulja = ((x - p) ** 2) + ((y - q) ** 2)
#         if izbrana == "elipsa":
#             a = random.randint(1, 4)
#             b = random.randint(1, 4)
#             r = 1  # definiran r zaradi različnega izpisa krivulj
#             krivulja = ((x - p) ** 2) / a**2 + ((y - q) ** 2) / b**2
#             if a == b:
#                 raise GeneratedDataIncorrect

#         razsirjena = a**2 * b**2 * krivulja.expand() - a**2 * b**2
#         return {
#             "razsirjena": sympy.Eq(razsirjena, 0),
#             "krivulja": sympy.Eq(krivulja, r**2),
#             "a": a,
#             "b": b,
#             "p": p,
#             "q": q,
#         }
