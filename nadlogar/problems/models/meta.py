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


class GeneratedDataIncorrect(Exception):
    pass


class Problem(models.Model):
    default_instruction = None
    default_solution = None
    document = models.ForeignKey("documents.Document", on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        limit_choices_to=limit_content_type_choices,
    )
    number_of_subproblems = models.PositiveSmallIntegerField(
        "število podnalog",
        help_text="Če je izbrana več kot ena naloga, bodo navodila našteta v seznamu.",
        default=1,
    )
    instruction = models.TextField("navodilo", blank=True)
    solution = models.TextField("rešitev", blank=True)

    class Meta:
        default_related_name = "problems"

    def __str__(self):
        return f"{self.document}: {self.content_type.name}"

    def clean(self):
        if issubclass(Problem, type(self)):
            raise ValidationError("Problems must have a non-trivial generator")
        self.content_type = ContentType.objects.get_for_model(type(self))

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

    def _generate_data(self, seed):
        data = []
        for i in range(self.number_of_subproblems):
            random.seed(f"{i}-{seed}")
            while True:
                try:
                    data.append(self.generate())
                    break
                except GeneratedDataIncorrect:
                    pass
        return data

    def uses_custom_text(self):
        return bool(self.instruction or self.solution)

    def render(self, data, default_text=False):
        if not default_text and self.uses_custom_text():
            instruction = self.instruction
            solution = self.solution
        else:
            instruction = self.default_instruction
            solution = self.default_solution
        rendered_texts = []
        for datum in data:
            rendered_instruction = Template(instruction).substitute(**datum)
            rendered_solution = Template(solution).substitute(**datum)
            rendered_texts.append(
                {"instruction": rendered_instruction, "solution": rendered_solution}
            )
        return rendered_texts

    def example_data(self):
        return self._generate_data(None)

    def example_text(self):
        data = self.example_data()
        return self.render(data)

    def student_text(self, student):
        seed = f"{self.id}-{student.id}"
        data = self._generate_data(seed)
        rendered_text = self.render(data)
        return rendered_text

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
