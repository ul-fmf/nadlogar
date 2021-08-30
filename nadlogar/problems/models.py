import random

import sympy
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models


def limit_content_type_choices():
    problem_subclasses = Problem.__subclasses__()
    content_types = ContentType.objects.get_for_models(*problem_subclasses).values()
    return {"id__in": {content_type.id for content_type in content_types}}


def generiraj_kompleksna_stevila(kolicina):
    stevila_r = random.choices(
        [x for x in range(-5, 6) if x != 0],
        k=kolicina,  # Izbere naključne realne dele
    )
    stevila_i = random.choices(
        [x for x in range(-5, 6) if x != 0],
        k=kolicina,  # Izbere naključne imaginarne dele
    )
    stevila = [r + i * sympy.I for r, i in zip(stevila_r, stevila_i)]

    if len(stevila) != len(
        set(stevila)
    ):  # preveri, da so vsa števila medsebojno različna
        raise GeneratedDataIncorrect

    if kolicina == 1:
        stevila = stevila[0]

    return stevila


class ProblemText(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        limit_choices_to=limit_content_type_choices,
    )
    question = models.TextField(blank=True)
    answer = models.TextField(blank=True)

    def __str__(self):
        return f"{self.content_type.name}: {self.question} / {self.answer}"

    def render(self, data):
        question = self.question.format(**data)
        answer = self.answer.format(**data)
        return question, answer


class GeneratedDataIncorrect(Exception):
    pass


class Problem(models.Model):
    quiz = models.ForeignKey("quizzes.Quiz", on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        limit_choices_to=limit_content_type_choices,
    )
    text = models.ForeignKey("problems.ProblemText", on_delete=models.PROTECT)

    class Meta:
        default_related_name = "problems"

    def __str__(self):
        return f"{self.quiz}: {self.content_type.name}"

    def clean(self):
        if issubclass(Problem, type(self)):
            raise ValidationError("Problems must have a non-trivial generator")
        self.content_type = ContentType.objects.get_for_model(type(self))
        if hasattr(self, "text") and self.content_type != self.text.content_type:
            raise ValidationError("Generators of the problem and its text must match")

    def save(self, *args, **kwargs):
        self.content_type = ContentType.objects.get_for_model(type(self))
        super().save(*args, **kwargs)

    def downcast(self):
        content_type = self.content_type
        if content_type.model_class() == type(self):
            return self
        return content_type.get_object_for_this_type(problem_ptr_id=self.id)

    def generate(self):
        raise NotImplementedError

    def validate(self, condition):
        if not condition:
            raise GeneratedDataIncorrect

    def generate_data(self, seed):
        random.seed(seed)
        generator = self.downcast()
        while True:
            try:
                return generator.generate()
            except GeneratedDataIncorrect:
                pass

    def generate_everything(self, student=None):
        seed = (self.id, None if student is None else student.id)
        data = self.generate_data(seed)
        question, answer = self.text.render(data)
        return data, question, answer


class ProstoBesedilo(Problem):
    """Problem s poljubnim fiksnim vprašanjem in odgovorom, namenjen ročno sestavljenim nalogam."""

    vprasanje = models.TextField("vprašanje", help_text="Poljubno besedilo vprašanja.")
    odgovor = models.TextField("odgovor", help_text="Poljubno besedilo odgovora.")

    class Meta:
        verbose_name = "prosto besedilo"

    def generate(self):
        return {
            "vprasanje": self.vprasanje,
            "odgovor": self.odgovor,
        }


class KrajsanjeUlomkov(Problem):
    """Problem, v katerem je treba okrajšati dani ulomek."""

    najvecji_stevec = models.PositiveSmallIntegerField(
        "največji števec",
        help_text="Največji števec, ki se bo pojavljal v okrajšanem ulomku.",
    )
    najvecji_imenovalec = models.PositiveSmallIntegerField(
        "največji imenovalec",
        help_text="Največji imenovalec, ki se bo pojavljal v okrajšanem ulomku.",
    )
    najvecji_faktor = models.PositiveSmallIntegerField(
        "največji faktor",
        help_text="Največji faktor med neokrajšanim in okrajšanim ulomkom.",
    )

    class Meta:
        verbose_name = "krajšanje ulomkov"

    def generate(self):
        stevec = random.randint(1, self.najvecji_stevec)
        imenovalec = random.randint(1, self.najvecji_imenovalec)
        faktor = random.randint(1, self.najvecji_faktor)
        return {
            "okrajsan_stevec": stevec,
            "okrajsan_imenovalec": imenovalec,
            "neokrajsan_stevec": faktor * stevec,
            "neokrajsan_imenovalec": faktor * imenovalec,
        }


class IskanjeNicelPolinoma(Problem):
    """Problem, v katerem je treba poiskati ničle danega polinoma."""

    stevilo_nicel = models.PositiveSmallIntegerField(
        "število ničel", help_text="Največje število ničel polinoma (vedno bo vsaj 1)."
    )
    velikost_nicle = models.PositiveSmallIntegerField(
        "velikost ničle",
        help_text="Največja velikost ničle glede na absolutno vrednost.",
    )

    class Meta:
        verbose_name = "iskanje ničel polinoma"

    def generate(self):
        nicla = random.randint(1, self.velikost_nicle)
        if self.stevilo_nicel % 2 == 0:
            nicle = {nicla, -nicla}
        else:
            nicle = {nicla}
        polinom = f"x^{self.stevilo_nicel} - {nicla ** self.stevilo_nicel}"
        return {"nicle": nicle, "polinom": polinom}


class RazstaviVieta(Problem):
    """Problem za razstavljanje s pomočjo Vietovega pravila."""

    maksimalna_vrednost = models.PositiveSmallIntegerField(
        "maksimalna vrednost",
        help_text="Največja možna vrednost razstavljenega člena glede na absolutno vrednost",
    )
    vodilni_koeficient = models.BooleanField(
        "vodilni koeficient", help_text="Ali naj bo vodilni koeficient različen od 1?"
    )

    class Meta:
        verbose_name = "razstavi Vieta"

    def generate(self):
        x1 = random.randint(-self.maksimalna_vrednost, self.maksimalna_vrednost)
        x2 = random.randint(-self.maksimalna_vrednost, self.maksimalna_vrednost)
        a = (
            random.choice([1, -1]) * random.randint(2, 4)
            if self.vodilni_koeficient
            else 1
        )

        x = sympy.symbols("x")
        razstavljen = sympy.Mul(a, (x - x1), (x - x2), evaluate=False).simplify()
        izraz = razstavljen.expand()

        return {"izraz": sympy.latex(izraz), "razstavljen": sympy.latex(razstavljen)}


class RazstaviRazliko(Problem):
    """Problem za razstavljanje razlike kvadratov, kubov in višjih potenc."""

    najmanjsa_potenca = models.PositiveSmallIntegerField(
        "najmanjša potenca", help_text="Najmanjša možna potenca za razstavljanje."
    )
    najvecja_potenca = models.PositiveSmallIntegerField(
        "največja potenca", help_text="Največja možna potenca za razstavljanje."
    )
    linearna_kombinacija = models.BooleanField(
        "linearna kombinacija",
        help_text="Ali naj naloga vsebuje linearno kombinacijo dveh neznank ali enostaven dvočlenik?",
    )

    class Meta:
        verbose_name = "razstavi razliko"

    def generate(self):
        if self.najmanjsa_potenca > self.najvecja_potenca:
            self.najmanjsa_potenca, self.najvecja_potenca = (
                self.najvecja_potenca,
                self.najmanjsa_potenca,
            )

        potenca = random.randint(self.najmanjsa_potenca, self.najvecja_potenca)
        if potenca == 2:
            do = 10
        else:
            do = 5
        simboli = ["a", "b", "c", "x", "y", "z", "v", "t"]
        izbran_simbol = random.choice(simboli)
        x = sympy.symbols(izbran_simbol)
        simboli.remove(izbran_simbol)
        if not self.linearna_kombinacija:
            a = 1
            b = random.choice([x for x in range(-do, do) if x != 0])
            y = 1
            m = 1
            n = 1
        else:
            a = random.randint(1, do)
            b = random.choice([x for x in range(-do, do) if x != 0])
            n = random.randint(1, 3)
            m = random.randint(1, 3)
            y = sympy.symbols(random.choice(simboli))
        izraz = (a * x ** n) ** potenca - (b * y ** m) ** potenca
        razstavljen = sympy.factor(izraz)

        return {"izraz": sympy.latex(izraz), "razstavljen": sympy.latex(razstavljen)}


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


class PotencaDvoclenika(Problem):
    """Problem za potenciranje dvočlenika."""

    najmanjsa_potenca = models.PositiveSmallIntegerField(
        "najmanjša potenca", help_text="Najmanjša možna potenca dvočlenika."
    )
    najvecja_potenca = models.PositiveSmallIntegerField(
        "največja potenca", help_text="Največja možna potenca dvočlenika."
    )
    linearna_kombinacija = models.BooleanField(
        "linearna kombinacija",
        help_text="Ali naj naloga vsebuje linearno kombinacijo dveh neznank ali enostaven dvočlenik?",
    )

    class Meta:
        verbose_name = "potenciranje dvočlenika"

    def generate(self):
        potenca = random.randint(self.najmanjsa_potenca, self.najvecja_potenca)
        simboli = ["a", "b", "c", "x", "y", "z", "v", "t"]
        izbran_simbol = random.choice(simboli)
        x = sympy.symbols(izbran_simbol)
        simboli.remove(izbran_simbol)
        if not self.linearna_kombinacija:
            a = 1
            b = random.choice([x for x in range(-5, 5) if x != 0])
            n = 1
            y = 1
            m = 1
        else:
            a = random.randint(1, 5)
            b = random.choice([x for x in range(-5, 5) if x != 0])
            n = random.randint(2, 5)
            m = random.randint(1, 5)
            y = sympy.symbols(random.choice(simboli))

        izraz = sympy.Pow(a * x ** n + b * y ** m, potenca, evaluate=False)
        return {
            "izraz": sympy.latex(izraz),
            "resitev": sympy.latex(sympy.expand(izraz)),
        }


class PotencaTroclenika(Problem):
    """Problem za potenciranje tročlenika."""

    najmanjsa_potenca = models.PositiveSmallIntegerField(
        "najmanjša potenca", help_text="Najmanjša možna potenca tročlenika."
    )
    najvecja_potenca = models.PositiveSmallIntegerField(
        "največja potenca", help_text="Največja možna potenca dvočlenika."
    )
    linearna_kombinacija = models.BooleanField(
        "linearna kombinacija",
        help_text="Ali naj naloga vsebuje linearno kombinacijo treh neznank ali enostaven tročlenik?",
    )

    class Meta:
        verbose_name = "potenciranje tročlenika"

    def generate(self):
        potenca = random.randint(self.najmanjsa_potenca, self.najvecja_potenca)
        simboli = [sympy.symbols(x) for x in ["a", "b", "c", "x", "y", "z", "v", "t"]]
        x, y, z = random.sample(simboli, 3)
        a = random.randint(1, 4)
        b = random.choice([x for x in range(-4, 4) if x != 0])
        c = random.choice([x for x in range(-4, 4) if x != 0])
        if not self.linearna_kombinacija:
            a = 1
            b = 1
            z = 1

        izraz = sympy.Pow(a * x + b * y + c * z, potenca, evaluate=False)
        return {
            "izraz": sympy.latex(izraz),
            "resitev": sympy.latex(sympy.expand(izraz)),
        }


class PotencaVecclenika(Problem):
    """Problem za potenciranje veččlenika."""

    najmanjsa_potenca = models.PositiveSmallIntegerField(
        "najmanjša potenca", help_text="Najmanjša možna potenca veččlenika."
    )
    najvecja_potenca = models.PositiveSmallIntegerField(
        "največja potenca", help_text="Največja možna potenca veččlenika."
    )
    najmanj_clenov = models.PositiveSmallIntegerField(
        "najmanj členov", help_text="Najmanjše možno število členov v veččleniku."
    )
    najvec_clenov = models.PositiveSmallIntegerField(
        "največ členov", help_text="Največje možno število členov v veččleniku."
    )
    linearna_kombinacija = models.BooleanField(
        "linearna kombinacija",
        help_text="Ali naj naloga vsebuje linearno kombinacijo neznank ali enostaven veččlenik?",
    )

    class Meta:
        verbose_name = "potenciranje veččlenika"

    def generate(self):
        potenca = random.randint(self.najmanjsa_potenca, self.najvecja_potenca)
        cleni = random.randint(self.najmanj_clenov, self.najvec_clenov)
        simboli = [
            sympy.symbols(chr(x)) for x in random.sample(range(97, 123), cleni)
        ]  # izberemo naključne znake abecede
        if potenca == 2:
            do = 10
        else:
            do = 5

        koeficienti = random.choices([x for x in range(-do, do) if x != 0], k=cleni)
        if not self.linearna_kombinacija:
            potence = [1 for _ in range(cleni)]
        else:
            potence = random.choices(range(1, 4), k=cleni)

        vrednosti = zip(koeficienti, simboli, potence)
        izraz = sympy.Pow(
            sum(k * s ** p for k, s, p in vrednosti), potenca, evaluate=False
        )

        return {
            "izraz": sympy.latex(izraz),
            "resitev": sympy.latex(sympy.expand(izraz)),
        }


class VsotaKompleksnih(Problem):
    """Problem za seštevanje in odštevanje kompleksnih števil."""

    class Meta:
        verbose_name = "vsota in razlika kompleksnih števil"

    def generate(self):
        kolicina = 3
        koeficienti_s = random.choices(
            range(1, 5),
            weights=(3, 1, 1, 1),
            k=kolicina,  # Izbere naključne števce, prednost ima 1
        )
        koeficienti_i = random.choices(
            range(1, 5),
            weights=(7, 1, 1, 1),
            k=kolicina,  # Izbere naključne imenovalce, prednost ima 1
        )
        koeficienti_p = random.choices(
            (-1, 1),
            weights=(1, 2),
            k=kolicina,  # Izbere naključne predznake, prednost ima pozitiven
        )
        koeficienti = [
            p * sympy.Rational(s, i)
            for p, s, i in zip(koeficienti_p, koeficienti_s, koeficienti_i)
        ]

        stevila = generiraj_kompleksna_stevila(kolicina)

        izraz = sympy.Add(
            *[sympy.Mul(k, z, evaluate=False) for k, z in zip(koeficienti, stevila)],
            evaluate=False,
        )
        resitev = sympy.simplify(izraz)

        return {
            "izraz": sympy.latex(izraz),
            "resitev": sympy.latex(resitev),
        }


class KompleksniUlomek(Problem):
    """Problem za seštevanje in racionalizacijo kompleksnih ulomkov."""

    class Meta:
        verbose_name = "seštevanje in racionalizacija kompleksnih ulomkov"

    def generate(self):
        kolicina = 4
        stevila = generiraj_kompleksna_stevila(kolicina)

        izraz = sympy.Add(
            sympy.Mul(
                stevila[0], sympy.Pow(stevila[1], -1, evaluate=False), evaluate=False
            ),
            sympy.Mul(
                stevila[2], sympy.Pow(stevila[3], -1, evaluate=False), evaluate=False
            ),
            evaluate=False,
        )
        resitev = sympy.simplify(izraz)

        return {
            "izraz": sympy.latex(izraz),
            "resitev": sympy.latex(resitev),
        }


class MnozenjeKompleksnih(Problem):
    """Problem za množenje kompleksnih števil."""

    class Meta:
        verbose_name = "množenje kompleksnih števil"

    def generate(self):
        kolicina = 2
        stevila = generiraj_kompleksna_stevila(kolicina)

        izraz = sympy.Mul(*stevila, evaluate=False)
        resitev = sympy.simplify(izraz)

        return {
            "izraz": sympy.latex(izraz),
            "resitev": sympy.latex(resitev),
        }


class RacunanjeKompleksno(Problem):
    """Problem za računanje absolutne vrednosti, potenciranja in konjugiranje kompleksnega števila ter višje potence kompleksne enote i."""

    class Meta:
        verbose_name = "računanje z kompleksno enoto"

    def generate(self):
        z = sympy.symbols("z")
        z0 = generiraj_kompleksna_stevila(1)
        izraz = (
            sympy.Pow(z, random.randint(2, 3))
            + sympy.Mul(
                sympy.Pow(sympy.I, random.randint(1991, 2018), evaluate=False),
                sympy.conjugate(z),
                evaluate=False,
            )
            + abs(z) ** 2
        )
        resitev = sympy.simplify(izraz.subs(z, z0))
        return {
            "stevilo": sympy.latex(z0),
            "izraz": sympy.latex(izraz),
            "resitev": sympy.latex(resitev),
        }


class KompleksnaEnacba(Problem):
    """Problem za množenja, konjugiranja, absolutne vrednosti in komponent kompleksnih števil."""

    konjugirana_vrednost = models.BooleanField(
        "konjugirana vrednost",
        help_text="Ali naj naloga vsebuje konjugirano vrednost?",
        choices=[(True, "Da"), (False, "Ne")],
    )

    class Meta:
        verbose_name = "enačbe s kompleksnimi števili"

    def generate(self):
        z = sympy.symbols("z")
        resitev, z1 = generiraj_kompleksna_stevila(2)
        if not self.konjugirana_vrednost:
            enacba = z1 * z
        else:
            z2 = generiraj_kompleksna_stevila(1)
            enacba = z1 * z + z2 * sympy.conjugate(z)
        z3 = sympy.simplify(enacba.subs(z, resitev))
        im = sympy.im(resitev)
        re = sympy.re(resitev)
        absolutna = abs(resitev)

        return {
            "enacba": sympy.latex(sympy.Eq(enacba, z3)),
            "resitev": sympy.latex(resitev),
            "imaginarna": sympy.latex(im),
            "realna": sympy.latex(re),
            "absolutna": sympy.latex(absolutna),
        }

