import random
import string

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

# This file describes the Problem class that is a parent class for classes describing
# particular problem kinds, which are implemented in other files.
#
# The main purpose of Nadlogar is to organize sets of mathematical problems, each with
# a given kind (eg. finding zeroes of a polynomial, computing set operations, ...) and
# parameters (number of zeroes, size of sets, ...). Since parameters vary with problem
# kinds, we need a separate table for each kind. However, we still want different
# problems to appear in a single document, thus we also need a single table containing
# all the problems. Also, there are a number of attributes that all problems have in
# common (document in which they appear, number of subproblems to generate, ...)
#
# To resolve this, we use Django's multi-table inheritance
# https://docs.djangoproject.com/en/4.1/topics/db/models/#multi-table-inheritance
# where each subproblem is stored in two places. All the common attributes are stored
# in a parent table, while the problem kind particular parameters are stored in a child
# table, one for each kind of a problem. Each entry in the child table additionally
# contains a foreign key to a corresponding entry in the parent table.
#
# In addition to what Django gives us, we want to store a link from the parent table
# to the child table. We store this information Django's ContentType mechanism
# https://docs.djangoproject.com/en/4.1/ref/contrib/contenttypes/
# which creates a database entry for each model class. Given a problem in the parent
# table, we can look up its content type, using that determine the appropriate child
# model, and finally look up the exact parameters in the child table.
#
# Each child class is equipped with a generate method that produces problem data, which
# is a dictionary of labels and corresponding values, for example
#     {"polynomial": "x^2 - 1", "zeroes": [-1, 1]}
# that is then inserted into a given template such as
#     "Find all the zeros of the polynomial @polynomial."
# to obtain an problem text such as
#     "Find all the zeros of the polynomial x^2 - 1."


def problem_content_types():
    """Returns a mapping of all problem kinds and their corresponding content types."""
    problem_subclasses = Problem.__subclasses__()
    return ContentType.objects.get_for_models(*problem_subclasses)


def limit_content_type_choices():
    """Returns a filter for content types foreign keys.

    Passing this to the limit_choices_to argument of a ForeignKey, ensure that those
    foreign keys can refer only to content types that correspond to problem kinds.
    """
    content_types = problem_content_types().values()
    return {"id__in": {content_type.id for content_type in content_types}}


class Template(string.Template):
    # Python standard library includes string.Template that can be used for string
    # templates in which $xyz can be substituted for a variable xyz. Since $ is
    # a common LaTeX symbol, we opt for @ instead so we override the class.
    delimiter = "@"


class GeneratedDataIncorrect(Exception):
    """An exception that is raised when a generator failed to produce proper problem data.

    Sometimes we can determine only after a few steps that the problem data in not suitable.
    For example, the zeroes of a polynomial may be sufficiently small, but after expanding the
    polynomial, the coefficients end up too large. In this case, we can raise
    GeneratedDataIncorrect to restart the generator with a different random seed.
    """

    pass


class Problem(models.Model):
    # Each problem has a default instruction and solution that are used unless specified
    # otherwise by the user.
    default_instruction = None
    default_solution = None
    document = models.ForeignKey("documents.Document", on_delete=models.CASCADE)
    # A content type of the problem kind this problem. When saving the model, we have to
    # make sure that the content type corresponds to the particular subclass.
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
        # We ensure that a problem is never saved using a parent class model.
        if issubclass(Problem, type(self)):
            raise ValidationError("Problems must have a non-trivial generator")
        # The content type is set automatically from the class.
        self.content_type = ContentType.objects.get_for_model(type(self))

    def save(self, *args, **kwargs):
        # The content type is set automatically from the class.
        self.content_type = ContentType.objects.get_for_model(type(self))
        super().save(*args, **kwargs)

    def downcast(self):
        """Converts an instance to its particular problem child class.

        This works even if we start with a problem from the parent table.
        """
        content_type = self.content_type
        # If the current type matches the content type, there is nothing to convert
        if content_type.model_class() == type(self):
            return self
        # Otherwise, we look up the object in the child table
        return content_type.get_object_for_this_type(problem_ptr_id=self.id)

    def generate(self):
        """Does a single attempt of generating problem data."""
        # All child classes must override this method as the parent class does not
        # generate anything.
        raise NotImplementedError

    def validate(self, condition):
        """An auxiliary method to raise GeneratedDataIncorrect if a condition fails."""
        if not condition:
            raise GeneratedDataIncorrect

    def _generate_data(self, seed):
        data = []
        for i in range(self.number_of_subproblems):
            # Ensure that the generated data is predictable, but still different
            # if multiple subproblems are generated.
            random.seed(f"{i}-{seed}")
            while True:
                # Repeat until suitable data is found
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
        """Creates a copy of a problem in a given document."""
        # We need to downcast in order to save an object of the correct class.
        # Since downcasting fetches a new instance from the database, we need to
        # do this first before changing any of the attributes.
        self = self.downcast()
        self.document = document
        # If this was an ordinary model, a copy is created by setting the primary key
        # to None, changing the document, and saving the model. But since we are dealing
        # with inheritance, we need to set both pk and id to None, and additionally
        # _state.adding to True.
        # https://docs.djangoproject.com/en/4.1/topics/db/queries/#copying-model-instances
        self.pk = None
        self.id = None
        self._state.adding = True
        self.save()
        return self
