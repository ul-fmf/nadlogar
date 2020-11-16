from django.db import models


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["date", "name"]
        verbose_name_plural = "quizzes"

    def __str__(self):
        return f"{self.name} ({self.date})"

    def generate_everything(self):
        return [
            problem.downcast().generate_everything() for problem in self.problems.all()
        ]
