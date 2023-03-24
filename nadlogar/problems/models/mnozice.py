import random

import sympy
from django.db import models

from .meta import Problem


class ElementiMnozice(Problem):
    """Problem za izpis elementov množice iz podanega predpisa."""

    default_instruction = "Zapiši elemente množice $ \\mathcal{A} = \\{ @n;  (n \\in \\mathbb{N}) \\land (n @pogoj @stevilo ) \\}$."
    default_solution = "$ \\mathcal{A} =@mnozica$"

    POGOJ = ["|", "<", "<="]
    POGOJ_LATEX = {"|": r"\mid", "<": r"\lt", "<=": r"\le"}

    linearna_kombinacija = models.BooleanField(
        "linearna kombinacija",
        help_text="Ali naj naloga vsebuje linearno kombinacijo?",
        choices=[(True, "Da"), (False, "Ne")],
        default=True,
    )

    class Meta:
        verbose_name = "Množice / elementi iz predpisa"

    def generate(self):
        pogoj = random.choice(self.POGOJ)
        n = sympy.symbols("n")
        if not self.linearna_kombinacija:
            a = 1
            b = 0
        else:
            a = random.randint(1, 3)
            b = random.randint(-2, 2)
        if pogoj == "|":
            stevilo = random.randint(15, 45)
            ustrezni = sympy.divisors(stevilo)
        elif pogoj == "<":
            stevilo = random.randint(5, 12)
            ustrezni = list(range(1, stevilo))
        elif pogoj == "<=":
            stevilo = random.randint(5, 8)
            ustrezni = list(range(1, stevilo + 1))
        mnozica = sympy.FiniteSet(*[a * x + b for x in ustrezni if a * x + b > 0])
        return {
            "n": sympy.latex(sympy.simplify(a * n + b)),
            "pogoj": self.POGOJ_LATEX[pogoj],
            "stevilo": sympy.latex(stevilo),
            "mnozica": sympy.latex(mnozica),
        }


class PotencnaMnozica(Problem):
    """Problem za izpis potenčne množice od dane množice."""

    default_instruction = "Zapiši potenčno množico množice $ \\mathcal{A} =@mnozica$"
    default_solution = "$\\mathcal{P}( \\mathcal{A} ) =@potencna$"

    class Meta:
        verbose_name = "Množice / potenčna množica"

    def generate(self):
        velikost = random.randint(2, 3)
        mnozice = [
            [sympy.Symbol("a"), sympy.Symbol("b"), sympy.Symbol("c")],
            [1, 2, 3],
            [sympy.Symbol("x"), sympy.Symbol("y"), sympy.Symbol("z")],
            [sympy.Symbol("alpha"), sympy.Symbol("beta"), sympy.Symbol("gamma")],
            [sympy.Symbol("Pi"), sympy.Symbol("Phi"), sympy.Symbol("Xi")],
            [3, 6, 9],
            [3, 7, 42],
        ]
        mnozica = sympy.FiniteSet(*random.choice(mnozice)[:velikost])
        potencna = mnozica.powerset()
        return {"mnozica": sympy.latex(mnozica), "potencna": sympy.latex(potencna)}


class OperacijeMnozic(Problem):
    """Naloga za zapis unije, preseka, razlike, in kartezičnega produkta množic."""

    default_instruction = "Dani sta množici $ \\mathcal{A} =@A$ in $ \\mathcal{B} =@B$.\r\n    Zapiši množice $ \\mathcal{A} \\cup  \\mathcal{B} $, $ \\mathcal{A} \\cap  \\mathcal{B} $, $ \\mathcal{A} - \\mathcal{B} $ in $ \\mathcal{A} \\times  \\mathcal{B} $."
    default_solution = "$ \\mathcal{A} \\cup  \\mathcal{B} =@unija$, $ \\mathcal{A} \\cap  \\mathcal{B} =@presek$, $ \\mathcal{A} - \\mathcal{B} =@brez$, $ \\mathcal{A} \\times  \\mathcal{B} =@kartezicno$"

    class Meta:
        verbose_name = "Množice / operacije z množicami"

    @staticmethod
    def generiraj_mnozico(velikost, od, do):
        """Pripravi naključno množico dane velikosti."""
        izbor = [x for x in range(od, do + 1)]
        mnozica = sympy.FiniteSet(*random.sample(izbor, velikost))
        return mnozica

    def generate(self):
        A = self.generiraj_mnozico(random.randint(3, 4), 1, 6)
        B = self.generiraj_mnozico(random.randint(3, 4), 1, 6)
        unija = A.union(B)
        presek = A.intersection(B)
        brez = sympy.Complement(A, B)
        kartezicno = sympy.FiniteSet(*A * B)
        return {
            "A": sympy.latex(A),
            "B": sympy.latex(B),
            "unija": sympy.latex(unija),
            "presek": sympy.latex(presek),
            "brez": sympy.latex(brez),
            "kartezicno": sympy.latex(kartezicno),
        }


class IzpeljaneMnozice(Problem):
    """Problem za zapis komplementa, unije in razlike množic ter izpis elementov izpeljane množice pri podani univerzalni množici."""

    default_instruction = "Dana je univerzalna množica $ \\mathcal{U} =\\mathbb{N}_{ @velikost_univerzalne }$ in njene pomnožice $ \\mathcal{A} =\\{ @navodilo_A; k \\in \\mathbb{N} \\}$, $ \\mathcal{B} = \\{ @navodilo_B; k \\in \\mathbb{N} \\}$, $ \\mathcal{C} =@C$. Zapiši elemente množic $ \\mathcal{A} $, $ \\mathcal{B} $, $ \\mathcal{A}  \\cup  \\mathcal{B} $, $ \\mathcal{C} ^{\\mathsf{c} }$ in $ \\mathcal{B}  -  \\mathcal{A} $."
    default_solution = "$ \\mathcal{A} =@A$, $ \\mathcal{B} =@B$, $ \\mathcal{A}  \\cup  \\mathcal{B}  =@A_unija_B$, $ \\mathcal{C} ^{\\mathsf{c} }=@C_komplement$,  $ \\mathcal{B}  -  \\mathcal{A}  =@B_brez_A$"

    class Meta:
        verbose_name = "Množice / operacije na izpeljanih množicah"

    def generate(self):
        k = sympy.symbols("k")
        a = random.randint(2, 5)
        b = random.randint(-4, 4)
        self.validate(abs(b) != a)
        c = random.randint(2, 5)
        d = random.randint(-4, 4)
        self.validate(abs(d) != c)
        velikost_univerzalne = random.randint(12, 20)
        univerzalna = sympy.FiniteSet(*range(1, velikost_univerzalne + 1))
        navodilo_A = a * k + b
        navodilo_B = c * k + d
        mnozica_A = [
            a * x + b
            for x in range(1, velikost_univerzalne + 1)
            if 0 < a * x + b <= velikost_univerzalne
        ]
        mnozica_B = [
            c * x + d
            for x in range(1, velikost_univerzalne + 1)
            if 0 < c * x + d <= velikost_univerzalne
        ]
        A = sympy.FiniteSet(*mnozica_A)
        B = sympy.FiniteSet(*mnozica_B)
        C = sympy.FiniteSet(*random.sample(sorted(univerzalna), 8))
        A_unija_B = A.union(B)
        C_komplement = sympy.Complement(univerzalna, C)
        B_brez_A = sympy.Complement(B, A)

        return {
            "navodilo_A": sympy.latex(navodilo_A),
            "navodilo_B": sympy.latex(navodilo_B),
            "A": sympy.latex(A),
            "B": sympy.latex(B),
            "C": sympy.latex(C),
            "A_unija_B": sympy.latex(A_unija_B),
            "C_komplement": sympy.latex(C_komplement),
            "B_brez_A": sympy.latex(B_brez_A),
            "velikost_univerzalne": sympy.latex(velikost_univerzalne),
        }
