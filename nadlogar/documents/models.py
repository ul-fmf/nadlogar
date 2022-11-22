import os
import subprocess
import tempfile

from django.db import models
from django.template import Context
from django.template import Template as DjangoTemplate
from django.utils.text import slugify

from . import izpit


class LaTeXError(Exception):
    pass


def _pdf_latex(source):
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, "izpit.cls"), "w") as izpit_cls_file:
            izpit_cls_file.write(izpit.cls)
        with tempfile.NamedTemporaryFile(dir=temp_dir, suffix=".tex") as temp_file:
            temp_file.write(source.encode())
            temp_file.flush()
            r = subprocess.run(
                ["pdflatex", "-interaction", "nonstopmode", temp_file.name],
                capture_output=True,
                cwd=temp_dir,
            )
            if r.returncode:
                raise LaTeXError(r.stdout, r.stderr)
            else:
                temp_pdf_name = temp_file.name.replace(".tex", ".pdf")
                with open(temp_pdf_name, "rb") as temp_pdf:
                    return temp_pdf.read()


class Template(models.Model):
    INDIVIDUAL = "I"
    GROUPED_BY_STUDENTS = "S"
    GROUPED_BY_PROBLEMS = "P"
    TYPE = [
        (INDIVIDUAL, "posamezna datoteka za vsakega učenca"),
        (
            GROUPED_BY_STUDENTS,
            "združena datoteka za vse učence, urejena po učencih",
        ),
        (
            GROUPED_BY_PROBLEMS,
            "združena datoteka za vse učence, urejena po nalogah",
        ),
    ]
    name = models.CharField("ime", max_length=255)
    template = models.TextField("predloga")
    type = models.CharField(
        max_length=1,
        choices=TYPE,
    )
    document_sort = models.ForeignKey(
        "documents.DocumentSort",
        verbose_name="vrsta dokumenta",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    def _file_name(self, document, student=None):
        if student is None:
            return f"{slugify(document.name)}/{slugify(self.name)}"
        else:
            return (
                f"{slugify(document.name)}/{slugify(self.name)}/{slugify(student.name)}"
            )

    def generate_files(self, document, student_problem_texts):
        template = DjangoTemplate(self.template)
        if self.type == self.INDIVIDUAL:
            for student, problem_texts in student_problem_texts.items():
                file_name = self._file_name(document, student) + ".tex"
                context = Context(
                    {
                        "document": document,
                        "student": {"name": student.name, "texts": problem_texts},
                    }
                )
                file_contents = template.render(context)
                yield (file_name, file_contents)
        elif self.type == self.GROUPED_BY_STUDENTS:
            file_name = self._file_name(document) + ".tex"
            students = [
                {"name": student.name, "texts": problem_texts}
                for student, problem_texts in student_problem_texts.items()
            ]
            context = Context({"document": document, "students": students})
            file_contents = template.render(context)
            yield (file_name, file_contents)
        elif self.type == self.GROUPED_BY_PROBLEMS:
            file_name = self._file_name(document) + ".tex"
            problems = [{"students": []} for _ in document.problems.all()]
            for student, problem_texts in student_problem_texts.items():
                for i, problem_text in enumerate(problem_texts):
                    problems[i]["students"].append(
                        {"name": student.name, "text": problem_text}
                    )
            context = Context({"document": document, "problems": problems})
            file_contents = template.render(context)
            yield (file_name, file_contents)


class DocumentSort(models.Model):
    name = models.CharField("ime", max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def tex_files(self, document, student_problem_texts):
        for template in self.template_set.all():
            yield from template.generate_files(document, student_problem_texts)


class Document(models.Model):
    name = models.CharField("ime", max_length=255)
    date = models.DateField(
        "datum dokumenta",
        help_text="Datum v glavi dokumenta in po katerem so urejeni dokumenti.",
    )
    sort = models.ForeignKey(
        "documents.DocumentSort", verbose_name="oblika", on_delete=models.PROTECT
    )
    introduction = models.TextField("uvodno besedilo", blank=True)
    student_group = models.ForeignKey(
        "students.StudentGroup", verbose_name="skupina", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-date", "name"]

    def __str__(self):
        return f"{self.name} ({self.date})"

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse(
            "students:documents:view_document",
            kwargs={"group_id": self.student_group.id, "document_id": self.id},
        )

    def generate_student_problem_texts(self):
        students = self.student_group.students
        student_problem_texts = {student: [] for student in students}
        for problem in self.problems.all():
            problem = problem.downcast()
            for student in students:
                _data, rendered_text = problem.generate_data_and_text(student)
                student_problem_texts[student].append(rendered_text)
        return student_problem_texts

    def problem_examples(self):
        for problem in self.problems.all():
            problem = problem.downcast()
            _, rendered_text = problem.generate_data_and_text()
            yield (problem, rendered_text)

    def tex_files(self):
        student_problem_texts = self.generate_student_problem_texts()
        yield from self.sort.tex_files(self, student_problem_texts)

    def pdf_files(self):
        for tex_file_name, tex_contents in self.tex_files():
            pdf_file_name = tex_file_name.replace(".tex", ".pdf")
            pdf_contents = _pdf_latex(tex_contents)
            yield pdf_file_name, pdf_contents

    def copy(self, group):
        old_problems = list(self.problems.all())
        self.student_group = group
        self.pk = None
        self.name += " (kopija)"
        self.save()
        for problem in old_problems:
            problem.copy(self)
        return self
