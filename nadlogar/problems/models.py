import random

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms import ModelForm


class Problem(models.Model):
    quiz = models.ForeignKey("quizzes.Quiz", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    question_template = models.TextField(blank=True)
    answer_template = models.TextField(blank=True)

    class Meta:
        default_related_name = "problems"
        verbose_name_plural = "problems"

    def __str__(self):
        return f"{self.quiz}: {self.content_type.name}"

    def save(self, **kwargs):
        if issubclass(Problem, type(self)):
            raise TypeError(
                "save() can be called only on instances of Problem sub-models"
            )
        self.content_type = ContentType.objects.get_for_model(type(self))
        super().save(**kwargs)

    @classmethod
    def form(cls):
        class ProblemForm(ModelForm):
            class Meta:
                model = cls
                exclude = ["quiz", "content_type"]

        return ProblemForm

    def downcast(self):
        content_type = self.content_type
        if content_type.model_class() == type(self):
            return self
        return content_type.get_object_for_this_type(problem_ptr_id=self.id)

    def generate_data(self):
        raise NotImplementedError

    @property
    def default_question_template(self):
        raise NotImplementedError

    @property
    def default_answer_template(self):
        raise NotImplementedError

    def answer(self, data):
        template = self.question_template or self.default_question_template
        return template.format(**data)

    def question(self, data):
        template = self.answer_template or self.default_answer_template
        return template.format(**data)

    def generate_everything(self):
        data = self.generate_data()
        question = self.answer(data)
        answer = self.question(data)
        return data, question, answer


class KrajsanjeUlomkov(Problem):
    najvecji_stevec = models.PositiveSmallIntegerField()
    najvecji_imenovalec = models.PositiveSmallIntegerField()
    najvecji_faktor = models.PositiveSmallIntegerField()

    def generate_data(self):
        stevec = random.randint(1, self.najvecji_stevec)
        imenovalec = random.randint(1, self.najvecji_imenovalec)
        faktor = random.randint(1, self.najvecji_faktor)
        return {
            "okrajsan_stevec": stevec,
            "okrajsan_imenovalec": imenovalec,
            "neokrajsan_stevec": faktor * stevec,
            "neokrajsan_imenovalec": faktor * imenovalec,
        }

    default_question_template = """
        Okrajšaj ulomek $\\frac{{{neokrajsan_stevec}}}{{{neokrajsan_imenovalec}}}$.
    """

    default_answer_template = """
        $\\frac{{{okrajsan_stevec}}}{{{okrajsan_imenovalec}}}$
    """


class IskanjeNicelPolinoma(Problem):
    stevilo_nicel = models.PositiveSmallIntegerField()
    velikost_nicle = models.PositiveSmallIntegerField()

    def generate_data(self):
        nicla = random.randint(1, self.velikost_nicle)
        if self.stevilo_nicel % 2 == 0:
            nicle = {nicla, -nicla}
        else:
            nicle = {nicla}
        polinom = f"x^{self.stevilo_nicel} - {nicla ** self.stevilo_nicel}"
        return {"nicle": nicle, "polinom": polinom}

    default_question_template = """
        Poišči vse ničle polonoma ${polinom}$.
    """

    default_answer_template = """
        ${nicle}$
    """
