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
    default_instruction = None
    default_solution = None
    document = models.ForeignKey("documents.Document", on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        limit_choices_to=limit_content_type_choices,
    )
    text = models.ForeignKey(
        "problems.ProblemText", on_delete=models.SET_NULL, blank=True, null=True
    )
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
        if self.text is not None and self.content_type != self.text.content_type:
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

    @classmethod
    def default_text(cls):
        return ProblemText(
            content_type=ContentType.objects.get_for_model(cls),
            instruction=cls.default_instruction,
            solution=cls.default_solution,
        )

    def _render_text(self, data):
        if self.text is None:
            return self.default_text().render(data)
        else:
            return self.text.render(data)

    def example_data(self):
        return self._generate_data(None)

    def example_text(self):
        data = self.example_data()
        return self._render_text(data)

    def student_text(self, student):
        seed = f"{self.id}-{student.id}"
        data = self._generate_data(seed)
        rendered_text = self._render_text(data)
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
