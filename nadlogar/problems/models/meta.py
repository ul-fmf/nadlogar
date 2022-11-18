import random
from string import Template as PythonTemplate

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
    instruction = models.TextField()
    solution = models.TextField()

    def __str__(self):
        return f"{self.content_type.name}: {self.instruction} / {self.solution}"

    def render(self, data):
        rendered_texts = []
        for datum in data:
            instruction = Template(self.instruction).substitute(**datum)
            solution = Template(self.solution).substitute(**datum)
            rendered_texts.append({"instruction": instruction, "solution": solution})
        return rendered_texts


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
    number_of_subproblems = models.PositiveSmallIntegerField(
        "število podnalog",
        help_text="Če je izbrana več kot ena naloga, bodo navodila našteta v seznamu.",
        default=1,
    )

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

    def generate_data(self, seed, count):
        data = []
        for i in range(count):
            random.seed(f"{i}-{seed}")
            while True:
                try:
                    data.append(self.generate())
                    break
                except GeneratedDataIncorrect:
                    pass
        return data

    def generate_data_and_text(self, student=None):
        seed = (self.id, None if student is None else student.id)
        data = self.generate_data(seed, self.number_of_subproblems)
        rendered_text = self.text.render(data)
        return data, rendered_text

    @classmethod
    def example_data_and_text(cls):
        problem = cls()
        content_type = ContentType.objects.get_for_model(cls)
        data = problem.generate_data(None, 1)
        text = ProblemText.objects.filter(content_type=content_type).first()
        rendered_text = text.render(data)
        return data[0], rendered_text

    def copy(self, document):
        self = self.downcast()
        self.document = document
        # https://docs.djangoproject.com/en/3.2/topics/db/queries/#copying-model-instances
        # > Due to how inheritance works, you have to set both pk and id to None, and _state.adding to True
        self.pk = None
        self.id = None
        self._state.adding = True
        self.save()
        return self
