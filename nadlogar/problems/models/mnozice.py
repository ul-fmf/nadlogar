from .meta import *


class ElementiMnozice(Problem):
    """Problem za izpis elementov množice iz podanega predpisa."""

    POGOJ = ["|", "<", "<="]
    POGOJ_LATEX = {"|": r"\mid", "<": r"\lt", "<=": r"\le"}

    linearna_kombinacija = models.BooleanField(
        "linearna kombinacija",
        help_text="Ali naj naloga vsebuje linearno kombinacijo?",
        choices=[(True, "Da"), (False, "Ne")],
    )

    class Meta:
        verbose_name = "elementi množice"

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

    class Meta:
        verbose_name = "potenčna množica"

    def generate(self):
        velikost = random.randint(2, 3)
        mnozice = [
            ["a", "b", "c"],
            [1, 2, 3],
            ["x", "y", "z"],
            ["alpha", "beta", "gamma"],
            ["Pi", "Phi", "Xi"],
            [3, 6, 9],
            [3, 7, 42],
        ]
        mnozica = sympy.FiniteSet(*random.choice(mnozice)[:velikost])
        potencna = mnozica.powerset()
        return {"mnozica": sympy.latex(mnozica), "potencna": sympy.latex(potencna)}


class OperacijeMnozic(Problem):
    """Naloga za zapis unije, preseka, razlike, in kartezičnega produkta množic."""

    class Meta:
        verbose_name = "operacije z množicami"

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

    class Meta:
        verbose_name = "izpeljane množice"

    def generate(self):
        k = sympy.symbols("k")
        a = random.randint(2, 5)
        b = random.randint(-4, 4)
        c = random.randint(2, 5)
        d = random.randint(-4, 4)
        if abs(b) == a or abs(d) == c:
            raise GeneratedDataIncorrect
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
        C = sympy.FiniteSet(*random.sample(set(univerzalna), 8))
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
