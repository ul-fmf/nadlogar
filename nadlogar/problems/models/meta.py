import random
from string import Template as PythonTemplate

import sympy
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models


def problem_content_types():
    problem_subclasses = Problem.__subclasses__()
    return ContentType.objects.get_for_models(*problem_subclasses)


def limit_content_type_choices():
    content_types = problem_content_types().values()
    return {"id__in": {content_type.id for content_type in content_types}}


class Template(PythonTemplate):
    delimiter = "@"


class ProblemText(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        limit_choices_to=limit_content_type_choices,
    )
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f"{self.content_type.name}: {self.question} / {self.answer}"

    def render(self, data):
        question = Template(self.question).substitute(**data)
        answer = Template(self.answer).substitute(**data)
        return {"question": question, "answer": answer}


class GeneratedDataIncorrect(Exception):
    pass


class Problem(models.Model):
    document = models.ForeignKey("documents.Document", on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        limit_choices_to=limit_content_type_choices,
    )
    text = models.ForeignKey("problems.ProblemText", on_delete=models.PROTECT)

    class Meta:
        default_related_name = "problems"

    def __str__(self):
        return f"{self.document}: {self.content_type.name}"

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
        while True:
            try:
                return self.generate()
            except GeneratedDataIncorrect:
                pass

    def generate_data_and_text(self, student=None):
        seed = (self.id, None if student is None else student.id)
        data = self.generate_data(seed)
        rendered_text = self.text.render(data)
        return data, rendered_text

    @staticmethod
    def example_data_and_text(content_type):
        problem = content_type.model_class()()
        data = problem.generate_data(None)
        text = ProblemText.objects.filter(content_type=content_type).first()
        return data, text.render(data)
