import enum
import random

import sympy

from .meta import GeneratedDataIncorrect, Problem

# Premisli, ali je ta razred smiselen, ker se tak tip podatkov načeloma shranjuje v slovarjih


class VrstaElementarneFunkcije(enum.Enum):
    """
    Razred vsebuje imena elementarnih funkcij.
    """

    RACIONALNA = "racionalna"
    POLINOM = "polinom"
    LOGARITEM = "logaritem"
    EKSPONENTNA = "eksponentna"
    KOTNA = "kotna"
    KROZNA = "krozna"


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

    generiraj_polinom(max_stopnja=5)
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


def izberi_logaritem_z_nakljucno_osnovo(osnove=[sympy.E, 2, 3, 4, 5, 10]):
    """
    Vrne naključno logaritemsko funkcijo z eno izmed podanih osnov.
    >>> izberi_logaritem_z_nakljucno_osnovo(osnove=[3,5])
    log(x)/log(5)
    """
    x = sympy.symbols("x")
    osnova = random.choice(osnove)
    if osnova == sympy.E:
        logaritem = sympy.ln(x)
    else:
        logaritem = sympy.simplify(sympy.log(x, osnova))
    return logaritem


def izberi_nakljucno_kotno_funkcijo():
    """
    Naključno izbere kosinus, sinus, tangens ali kotangens.
    """
    x = sympy.symbols("x")
    kosinus = sympy.cos(x)
    sinus = sympy.sin(x)
    tangens = sympy.tan(x)
    kotangens = sympy.cot(x)
    return random.choice([kosinus, sinus, tangens, kotangens])


def izberi_nakljucno_krozno_funkcijo():
    """
    Naključno izbere arkus kosinus, arkus sinus, arkus tangens ali arkus kotangens.
    """
    x = sympy.symbols("x")
    arcus_kosinus = sympy.acos(x)
    arcus_sinus = sympy.asin(x)
    arcus_tangens = sympy.atan(x)
    arcus_kotangens = sympy.acot(x)
    return random.choice([arcus_kosinus, arcus_sinus, arcus_tangens, arcus_kotangens])


class KotMedPremicama(Problem):
    """
    Naloga za izračun kota med dvema premicama.
    """

    default_instruction = r"Izračunaj kot, ki ga oklepata $y=@premica1$ in $@premica2$."
    default_solution = r"$\varphi =@stopinje^{\circ}@minute' $"

    class Meta:
        verbose_name = "Odvodi / računanje kota med premicama"

    def generate(self):
        x = sympy.symbols("x")
        y = sympy.symbols("y")
        k1, k2 = random.sample([x for x in range(-6, 7) if x != 0], 2)
        n1, n2 = random.sample([x for x in range(-10, 11) if x != 0], 2)
        premica1 = k1 * x + n1
        premica2 = sympy.Eq(y, k2 * x + n2)
        kot = sympy.N(sympy.deg(kot_med_premicama(k1, k2)))
        stopinje = kot // 1
        minute = round(kot % 1 * 60)
        return {
            "premica1": sympy.latex(premica1),
            "premica2": sympy.latex(premica2),
            "stopinje": sympy.latex(stopinje),
            "minute": sympy.latex(minute),
        }


class OdvodKompozitumaElementarnih(Problem):
    """
    Naloga za odvajanje kompozituma 2 izbranih elementarnih funkcij iz podanega seznama.
    """

    default_instruction = r"Določi odvod funkcije $f(x)=@kompozitum_funkcij$."
    default_solution = r"$f'(x)=@odvod_kompozituma$"

    class Meta:
        verbose_name = "Odvodi / odvajanje kompozituma funkcij"

    funkcije = [
        VrstaElementarneFunkcije.POLINOM,
        VrstaElementarneFunkcije.RACIONALNA,
        VrstaElementarneFunkcije.EKSPONENTNA,
        VrstaElementarneFunkcije.LOGARITEM,
        VrstaElementarneFunkcije.KOTNA,
    ]

    def generate(self):
        x = sympy.symbols("x")
        prva_elementarna = random.choice(self.funkcije)
        druga_elementarna = random.choice(
            [x for x in self.funkcije if x != VrstaElementarneFunkcije.RACIONALNA]
        )

        # TODO V Python 3.10 se tole da narediti s switch statementom
        # Poleg tega se da polovico te kode skrajšati

        vrsti_dveh_elementarnih = {prva_elementarna: None, druga_elementarna: None}
        for vrsta in vrsti_dveh_elementarnih:
            if vrsta.value == "polinom":
                vrsti_dveh_elementarnih[vrsta] = generiraj_polinom()
            elif vrsta.value == "racionalna":
                vrsti_dveh_elementarnih[vrsta] = generiraj_racionalno(
                    max_stopnja_stevca=2, max_stopnja_imenovalca=2
                )
            elif vrsta.value == "eksponentna":
                vrsti_dveh_elementarnih[vrsta] = generiraj_eksponentno()
            elif vrsta.value == "logaritem":
                vrsti_dveh_elementarnih[vrsta] = izberi_logaritem_z_nakljucno_osnovo(
                    osnove=[sympy.E]
                )
            elif vrsta.value == "kotna":
                vrsti_dveh_elementarnih[vrsta] = izberi_nakljucno_kotno_funkcijo()
            elif vrsta.value == "krozna":
                vrsti_dveh_elementarnih[vrsta] = izberi_nakljucno_krozno_funkcijo()

        zunanja_funkcija = vrsti_dveh_elementarnih[prva_elementarna]
        notranja_funkcija = vrsti_dveh_elementarnih[druga_elementarna]
        kompozitum_funkcij = zunanja_funkcija.subs(x, notranja_funkcija)
        odvod_kompozituma = kompozitum_funkcij.diff(x)
        return {
            "kompozitum_funkcij": sympy.latex(kompozitum_funkcij, ln_notation=True),
            "odvod_kompozituma": sympy.latex(odvod_kompozituma, ln_notation=True),
        }


# Tale naloga z odvodi ne dela prav, verižno pravilo ni prav sprogramirano


class OdvodSestavljene(Problem):
    """
    Naloga za odvajanje sestavljene funkcije iz podanega seznama elementarnih funkcij.
    """

    default_instruction = r"Določi odvod funkcije $f(x)=@funkcija$."
    default_solution = r"$f'(x)=@odvod$"

    class Meta:
        verbose_name = "Odvodi / odvajanje sestavljene funkcije"

    funkcije = [
        VrstaElementarneFunkcije.POLINOM,
        VrstaElementarneFunkcije.RACIONALNA,
        VrstaElementarneFunkcije.EKSPONENTNA,
        VrstaElementarneFunkcije.LOGARITEM,
        VrstaElementarneFunkcije.KOTNA,
    ]

    operatorji = [
        lambda a, b: a + b,
        lambda a, b: a - b,
        lambda a, b: a * b,
        lambda a, b: a / b,
    ]

    def generate(self):
        x = sympy.symbols("x")
        prva_elementarna = random.choice(self.funkcije)
        druga_elementarna = random.choice(self.funkcije)
        operator = random.choice(self.operatorji)

        vrsti_dveh_elementarnih = {prva_elementarna: None, druga_elementarna: None}
        for vrsta in vrsti_dveh_elementarnih:
            match vrsta.value:
                case "polinom":
                    vrsti_dveh_elementarnih[vrsta] = generiraj_polinom(
                        min_stopnja=1, max_stopnja=2
                    )
                case "racionalna":
                    vrsti_dveh_elementarnih[vrsta] = generiraj_racionalno(
                        max_stopnja_stevca=2, max_stopnja_imenovalca=2
                    )
                case "eksponentna":
                    vrsti_dveh_elementarnih[vrsta] = generiraj_eksponentno()
                case "logaritem":
                    vrsti_dveh_elementarnih[
                        vrsta
                    ] = izberi_logaritem_z_nakljucno_osnovo(osnove=[sympy.E])
                case "kotna":
                    vrsti_dveh_elementarnih[vrsta] = izberi_nakljucno_kotno_funkcijo()
                case "krozna":
                    vrsti_dveh_elementarnih[vrsta] = izberi_nakljucno_krozno_funkcijo()

        zunanja_funkcija = vrsti_dveh_elementarnih[prva_elementarna]
        notranja_funkcija = vrsti_dveh_elementarnih[druga_elementarna]

        zunanja_funkcija = zunanja_funkcija.subs(
            x, random.choice([-3, -2, -1, 2, 3, 4, 5]) * x
        )
        if zunanja_funkcija == notranja_funkcija:
            raise GeneratedDataIncorrect

        funkcija = operator(zunanja_funkcija, notranja_funkcija)
        odvod = sympy.simplify(sympy.simplify(funkcija).diff(x))
        return {
            "funkcija": sympy.latex(funkcija, ln_notation=True),
            "odvod": sympy.latex(odvod, ln_notation=True),
        }


class Tangenta(Problem):
    """
    Naloga za izračun tangente na graf v določeni točki.
    """

    default_instruction = r"Zapiši enačbo tangente na graf funkcije $f(x)=@funkcija$ v točki z absciso $x_0=@abscisa$."
    default_solution = r"$f'(x)=@tangenta$"

    class Meta:
        verbose_name = "Odvodi / enačba tangente na graf v določeni točki"

    funkcije = [
        VrstaElementarneFunkcije.POLINOM,
        VrstaElementarneFunkcije.RACIONALNA,
        VrstaElementarneFunkcije.EKSPONENTNA,
        VrstaElementarneFunkcije.LOGARITEM,
        VrstaElementarneFunkcije.KOTNA,
    ]

    def generate(self):
        x = sympy.symbols("x")
        izbrana = random.choice(self.funkcije)

        match izbrana.value:
            case "polinom":
                funkcija = generiraj_polinom()
                x0 = random.randint(-2, 2)
            case "racionalna":
                stopnja_stevca = random.randint(1, 2)
                stopnja_imenovalca = 2 - stopnja_stevca
                funkcija = generiraj_racionalno(
                    min_stopnja_stevca=stopnja_stevca,
                    max_stopnja_stevca=stopnja_stevca,
                    min_stopnja_imenovalca=stopnja_imenovalca,
                    max_stopnja_imenovalca=stopnja_imenovalca,
                )
                x0 = random.randint(-2, 2)
            case "eksponentna":
                osnova = random.choice([sympy.E, 2, 3, 5])
                funkcija = generiraj_eksponentno(osnove=[osnova])
                x0 = random.choice([sympy.log(n, osnova) for n in [1, 2, 3]])

            case "logaritem":
                funkcija = izberi_logaritem_z_nakljucno_osnovo(osnove=[sympy.E])
                x0 = sympy.E ** (random.randint(-1, 2))
            case "kotna":
                funkcija = izberi_nakljucno_kotno_funkcijo()
                x0 = random.choice([sympy.pi / x for x in [6, 3, 4, 2]])
            case "krozna":
                arcus_kosinus = sympy.acos(x)
                arcus_sinus = sympy.asin(x)
                x0 = random.choice([0, 1 / 2, sympy.sqrt(2) / 2, sympy.sqrt(3) / 2, 1])
                funkcija = random.choice([arcus_kosinus, arcus_sinus])
        odvod = sympy.simplify(funkcija).diff(x)
        y0 = funkcija.subs(x, x0)
        k = odvod.subs(x, x0)
        zacetna_vrednost = y0 - k * x0
        tangenta = k * x + zacetna_vrednost
        return {
            "funkcija": sympy.latex(funkcija),
            "abscisa": sympy.latex(x0),
            "tangenta": sympy.latex(tangenta),
        }


class KotMedGrafomaElementarnihFunkcij(Problem):
    """
    Naloga za izračun kota med grafoma dveh funkcij (kvadratnih, logaritmov ali eksponentnih).
    """

    default_instruction = r"Na minuto natančno izračunaj kot med grafoma funkcij $f(x)=@funkcija1$ in $g(x)=@funkcija2$."
    default_solution = r"$\varphi =@stopinje^{\circ}@minute'$"

    class Meta:
        verbose_name = "Odvodi / računanje kota med elementarnimi funkcijami"

    def generate(self):
        x = sympy.symbols("x", real=True)
        izbor = random.choice(["kvadratna", "eksponentna", "logaritem"])
        match izbor:
            case "eksponentna":
                osnova = random.choice([sympy.E, 2, 3, 5])
                eksponentna = osnova**x
                a = random.randint(1, 2)
                eksponent1 = sympy.Poly([a, random.randint(-3, 3)], x).as_expr()
                eksponent2 = sympy.Poly([-a, random.randint(-3, 3)], x).as_expr()
                funkcija1 = eksponentna.subs(x, eksponent1)
                funkcija2 = eksponentna.subs(x, eksponent2)
                presek = sympy.solve((eksponent1 - eksponent2), x)
                # Poenostavljen presek, ker sympy ne zna izračunati vseh eksponentnih enačb
            case "logaritem":
                naravni_logaritem = sympy.ln(x)
                a = random.randint(1, 2)
                funkcija1 = naravni_logaritem.subs(
                    x, sympy.Poly([a, random.randint(-3, 3)], x).as_expr()
                )
                funkcija2 = naravni_logaritem.subs(
                    x, sympy.Poly([-a, random.randint(-3, 3)], x).as_expr()
                )
                presek = sympy.solve((funkcija1 - funkcija2), x)
            case "kvadratna":
                x0 = random.choice([-2, -1, 1, 2])
                y0 = random.randint(-2, 2)
                a = random.randint(1, 2)
                c1 = random.randint(-4, -1)
                c2 = random.randint(0, 4)
                b1 = (y0 - a * x0**2 - c1) // x0
                b2 = (y0 - a * x0**2 - c2) // x0
                funkcija1 = sympy.Poly([a, b1, c1], x).as_expr()
                funkcija2 = sympy.Poly([a, b2, c2], x).as_expr()
                presek = sympy.solve((funkcija1 - funkcija2), x)
        if len(presek) != 1:
            raise GeneratedDataIncorrect
        k1 = funkcija1.diff().subs(x, *presek)
        k2 = funkcija2.diff().subs(x, *presek)
        kot = sympy.N(sympy.deg(kot_med_premicama(k1, k2)))
        stopinje = kot // 1
        minute = round(kot % 1 * 60)
        return {
            "funkcija1": sympy.latex(funkcija1),
            "funkcija2": sympy.latex(funkcija2),
            "stopinje": sympy.latex(stopinje),
            "minute": sympy.latex(minute),
        }
