from django.db import models
from django.template import Context
from django.template import Template as DjangoTemplate


class Template(models.Model):
    INDIVIDUAL = "I"
    GROUPED_BY_STUDENTS = "S"
    TYPE = [
        (INDIVIDUAL, "posamezna datoteka za vsakega študenta"),
        (
            GROUPED_BY_STUDENTS,
            "združena datoteka za vse študente, urejena po študentih",
        ),
    ]
    name = models.CharField("ime", max_length=255)
    template = models.TextField("predloga")
    type = models.CharField(
        max_length=1,
        choices=TYPE,
    )

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    def _file_name(self, document, student=None):
        if student is None:
            return f"{document.name}/{self.name}.pdf"
        else:
            return f"{document.name}/{self.name}/{student.name}.pdf"

    def generate_files(self, document, student_problem_texts):
        template = DjangoTemplate(self.template)
        if self.type == self.INDIVIDUAL:
            for student, problem_texts in student_problem_texts.items():
                file_name = self._file_name(document, student)
                context = Context(
                    {
                        "document": document,
                        "student": {"name": student.name, "texts": problem_texts},
                    }
                )
                file_contents = template.render(context)
                yield (file_name, file_contents)
        elif self.type == self.GROUPED_BY_STUDENTS:
            file_name = self._file_name(document)
            students = [
                {"name": student.name, "texts": problem_texts}
                for student, problem_texts in student_problem_texts.items()
            ]
            context = Context({"document": document, "students": students})
            file_contents = template.render(context)
            yield (file_name, file_contents)


class Document(models.Model):
    name = models.CharField("ime", max_length=255)
    date = models.DateField("datum")
    description = models.TextField("opis", blank=True)
    student_group = models.ForeignKey(
        "students.StudentGroup", verbose_name="skupina", on_delete=models.CASCADE
    )
    templates = models.ManyToManyField("documents.Template", verbose_name="predloge")

    class Meta:
        ordering = ["date", "name"]

    def __str__(self):
        return f"{self.name} ({self.date})"

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse(
            "students:documents:view_document",
            kwargs={"group_id": self.student_group.id, "document_id": self.id},
        )

    def generate_student_problem_texts(self):
        students = self.student_group.students.all()
        student_problem_texts = {student: [] for student in students}
        for index, problem in enumerate(self.problems.all(), 1):
            problem = problem.downcast()
            for student in students:
                _data, rendered_text = problem.generate_data_and_text(student)
                rendered_text["index"] = index
                student_problem_texts[student].append(rendered_text)
        return student_problem_texts

    def problem_examples(self):
        for problem in self.problems.all():
            problem = problem.downcast()
            data, rendered_text = problem.generate_data_and_text()
            yield (problem, data, rendered_text)

    def generate_files(self):
        student_problem_texts = self.generate_student_problem_texts()
        for template in self.templates.all():
            yield from template.generate_files(self, student_problem_texts)
