import random

import sympy

from .meta import GeneratedDataIncorrect, Problem


def naredi_eksponentno(do=3, cela_osnova=False, premik=0):
    """
    Funkcija vrne naključno eksponentno funkcijo, ki ustreza vpisanim pogojem.
    """

    x = sympy.symbols("x")
    izbor = list(range(2, do + 1))
    if not cela_osnova:
        izbor += (
            [sympy.Rational(x, 2) for x in range(1, 2 * (do)) if x != 2]
            + [sympy.Rational(x, 3) for x in range(1, 3 * (do)) if x != 3]
            + [sympy.Rational(x, 4) for x in range(1, 4 * (do)) if x != 4]
            + [sympy.Rational(x, 5) for x in range(1, 5 * (do)) if x != 5]
        )
    osnova = random.choice(izbor)
    return (osnova, premik, sympy.Add(sympy.Pow(osnova, x), premik, evaluate=False))


# class GrafEksponentne(Problem):
#     """
#     Naloga iz risanja dveh grafov eksponentne funkcije.
#     """

#     default_instruction = r"""V isti koordinatni sistem nariši grafa funkcij $f(x)=@eksponentna_prva$ in $g(x)=@eksponentna_druga$."""
#     # TODO izpisovanje imena funkcij na grafu
#     default_solution = r"""$f(x)=@eksponentna_prva$, $g(x)=@eksponentna_druga$ $\par
#     \begin{minipage}{\linewidth}
#     \centering
#     \begin{tikzpicture}[baseline]
#     \begin{axis}[axis lines=middle, xlabel=$x$, ylabel=$y$,
#     xtick={-5,-4,...,5}, ytick={-5,-4,...,5},
#     restrict y to domain=-5.5:5.5,
#     xmin=-5.5, xmax=5.5, ymin=-5.5, ymax=5.5,]
#     \addplot[domain =-5.5:5.5, color=black, smooth]{ {{naloga.narisi_eksponentna1}} } node[right, pos=1]{ {{latex(naloga.eksponentna1)}} };
#     \addplot[domain =-5.5:5.5, color=black, smooth]{ {{naloga.narisi_eksponentna2}} } node[right, pos=0.98]{ {{latex(naloga.eksponentna2)}}};
#     \addplot[domain =-5.5:5.5, color=black, dashed]{ {{naloga.premik2}} };
#     \end{axis}
#     \end{tikzpicture}
#     \end{minipage}$"""

#     class Meta:
#         verbose_name = "Eksponentna funkcija / risanje grafa"

#     def generate(self):
#         x = sympy.symbols("x")
#         osnova, premik, eksponentna_prva = naredi_eksponentno(
#             premik=random.choice([i for i in range(-3, 4) if i != 0]), cela_osnova=True
#         )
#         predznak = random.choice([1, -1])
#         premik_drugi = random.choice([x for x in range(-3, 4) if x != 0])
#         eksponentna_druga = sympy.Add(
#             predznak * sympy.Pow(osnova, x, evaluate=False),
#             premik_drugi,
#             evaluate=False,
#         )
#         narisi_eksponentna_prva = str(eksponentna_prva).replace("**", "^")
#         narisi_eksponentna_druga = str(eksponentna_druga).replace("**", "^")
#         return {
#             "eksponentna_prva": sympy.latex(eksponentna_prva),
#             "eksponentna_druga": sympy.latex(eksponentna_druga),
#             "narisi_eksponentna_prva": sympy.latex(narisi_eksponentna_prva),
#             "narisi_eksponentna_druga": sympy.latex(narisi_eksponentna_druga),
#             "premik_drugi": sympy.latex(premik_drugi),
#         }


class ResevanjeEksponentneEnacbe(Problem):
    """
    Naloga za reševanje eksponentne enačbe z eno osnovo.
    """

    # TODO tukaj bi se dalo izboljšati pogoje, da recimo sprejmemo samo celoštevilke rešitve ali kaj podobnega

    default_instruction = r"""Reši eksponentno enačbo $@enacba$."""
    default_solution = r"""$x=@resitev$."""

    class Meta:
        verbose_name = (
            "Eksponentna funkcija / reševanje eksponentne enačbe z eno osnovo"
        )

    def generate(self):
        x = sympy.symbols("x")
        osnova = random.choice([2, 3, 4, 5, 10])
        zamik_clena1 = random.choice([-3, -2, -1, 1, 2, 3])
        zamik_clena2 = random.choice([-3, -2, -1, 1, 2, 3])
        k_clena2 = random.choice([1, 2, 3, -1, -2, -3])
        resitev = random.choice([-1, 0, 1, 2, 3])
        if not (-2 < (resitev + zamik_clena1) and -2 < (resitev + zamik_clena2)):
            raise GeneratedDataIncorrect
        vrednost = sympy.Rational(
            osnova ** (resitev + zamik_clena1)
            + k_clena2 * (osnova) ** (resitev + zamik_clena2)
        )
        enacba = sympy.Eq(
            sympy.Pow(osnova, (x + zamik_clena1))
            + k_clena2 * sympy.Pow(osnova, (x + zamik_clena2)),
            vrednost,
        )

        return {"enacba": sympy.latex(enacba), "resitev": sympy.latex(resitev)}


class ResevanjeEksponentneEnacbeZDvemaOsnovama(Problem):
    """
    Naloga enačbe, kjer imata potenci dve različni osnovi.
    """

    default_instruction = r"""Reši eksponentno enačbo $@enacba$."""
    default_solution = r"""$x=@resitev$"""

    class Meta:
        verbose_name = (
            "Eksponentna funkcija / reševanje eksponentne enačbe z različnima osnovama"
        )

    # TODO Ta funkcija daje zelo nenavadne in nenaravne naloge. Morda jo je treba popraviti.

    def generate(self):
        [osnova1, osnova2] = random.sample([2, 3, 5, 7, 10], 2)
        x = sympy.symbols("x")
        u = random.choice([0, 1, 2, 3])
        v = random.choice([0, 1, 2, 3])
        # V primeru, da imamo kako osnovo 7 ali 10, nekoliko omejimo zamik, da ne pridejo prevelike vrednosti.
        if max(osnova1, osnova2) > 5:
            komponenta1_zamika_enacbe1 = random.randint(-3, 3)
        else:
            komponenta1_zamika_enacbe1 = random.randint(-5, 5)
        komponenta2_zamika_enacbe1 = random.choice([1, 2])
        komponenta1_zamika_enacbe2 = komponenta1_zamika_enacbe1 - v + u
        komponenta2_zamika_enacbe2 = random.choice([1, 2])
        k_osnove1_levi = random.choice([1, 2, 3, 4, 5])
        k_osnove1_desni = random.choice([1, 2, 3, 4, 5])
        k_osnove2_levi = (
            osnova2**u - osnova1**komponenta2_zamika_enacbe1 * k_osnove1_levi
        )
        k_osnove2_desni = (
            osnova1**v - osnova2**komponenta2_zamika_enacbe2 * k_osnove1_desni
        )
        resitev = v - komponenta1_zamika_enacbe1
        enacba = sympy.Eq(
            sympy.simplify(
                k_osnove1_levi
                * osnova1
                ** (x + komponenta1_zamika_enacbe1 + komponenta2_zamika_enacbe1)
                - k_osnove1_desni
                * osnova2
                ** (x + komponenta1_zamika_enacbe2 + komponenta2_zamika_enacbe2),
                rational=True,
            ),
            sympy.simplify(
                -k_osnove2_levi * osnova1 ** (x + komponenta1_zamika_enacbe1)
                + k_osnove2_desni * osnova2 ** (x + komponenta1_zamika_enacbe2),
                rational=True,
            ),
        )
        if not (max([abs(k_osnove2_levi), abs(k_osnove2_desni)]) < 50):
            raise GeneratedDataIncorrect  # Zagotovi, da v enačbi ne nastopajo prevelike vrednosti.
        return {"enacba": sympy.latex(enacba), "resitev": sympy.latex(resitev)}
