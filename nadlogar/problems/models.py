import random

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
    vprasanje = models.TextField()
    odgovor = models.TextField()

    def generate(self):
        return {
            "vprasanje": self.vprasanje,
            "odgovor": self.odgovor,
        }


class KrajsanjeUlomkov(Problem):
    najvecji_stevec = models.PositiveSmallIntegerField()
    najvecji_imenovalec = models.PositiveSmallIntegerField()
    najvecji_faktor = models.PositiveSmallIntegerField()

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
    stevilo_nicel = models.PositiveSmallIntegerField()
    velikost_nicle = models.PositiveSmallIntegerField()

    def generate(self):
        nicla = random.randint(1, self.velikost_nicle)
        if self.stevilo_nicel % 2 == 0:
            nicle = {nicla, -nicla}
        else:
            nicle = {nicla}
        polinom = f"x^{self.stevilo_nicel} - {nicla ** self.stevilo_nicel}"
        return {"nicle": nicle, "polinom": polinom}
