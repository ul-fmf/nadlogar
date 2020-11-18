from django.db import models


class StudentGroup(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey("students.StudentGroup", on_delete=models.CASCADE)

    class Meta:
        default_related_name = "students"
        ordering = ["group", "name"]

    def __str__(self):
        return f"{self.name} ({self.group})"
