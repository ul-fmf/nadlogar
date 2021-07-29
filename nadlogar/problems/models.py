import random

import sympy
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models


def limit_content_type_choices():
    problem_subclasses = Problem.__subclasses__()
    content_types = ContentType.objects.get_for_models(*problem_subclasses).values()
    return {"id__in": {content_type.id for content_type in content_types}}


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
