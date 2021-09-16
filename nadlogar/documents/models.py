from django.db import models


class Document(models.Model):
    name = models.CharField("ime", max_length=255)
    date = models.DateField("datum")
    description = models.TextField("opis", blank=True)
    student_group = models.ForeignKey(
        "students.StudentGroup", verbose_name="skupina", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["date", "name"]
        verbose_name_plural = "documents"

    def __str__(self):
        return f"{self.name} ({self.date})"

    def generate_data_and_text(self):
        students = self.student_group.students.all()
        student_documents = {student: [] for student in students}
        for problem in self.problems.all():
            for student in students:
                student_documents[student].append(
                    problem.generate_data_and_text(student)
                )
        return student_documents

    def problem_examples(self):
        examples = []
        for problem in self.problems.all():
            data, rendered_text = problem.generate_data_and_text()
            examples.append((problem, data, rendered_text))
        return examples
