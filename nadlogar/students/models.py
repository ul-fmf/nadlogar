from django.conf import settings
from django.db import models


class StudentGroup(models.Model):
    name = models.CharField("ime", max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField("ime", max_length=255)
    group = models.ForeignKey(
        "students.StudentGroup", verbose_name="skupina", on_delete=models.CASCADE
    )

    class Meta:
        default_related_name = "students"
        ordering = ["group", "name"]

    def __str__(self):
        return f"{self.name} ({self.group})"
