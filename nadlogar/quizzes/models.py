from django.db import models


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField(blank=True)
    student_group = models.ForeignKey("students.StudentGroup", on_delete=models.CASCADE)

    class Meta:
        ordering = ["date", "name"]
        verbose_name_plural = "quizzes"

    def __str__(self):
        return f"{self.name} ({self.date})"

    def generate_everything(self):
        students = self.student_group.students.all()
        student_quizzes = {student: [] for student in students}
        for problem in self.problems.all():
            for student in students:
                student_quizzes[student].append(problem.generate_everything(student))
        return student_quizzes

    def problem_examples(self):
        examples = []
        for problem in self.problems.all():
            data, question, answer = problem.generate_everything()
            examples.append((problem, data, question, answer))
        return examples
