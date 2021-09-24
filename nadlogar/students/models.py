from django.conf import settings
from django.db import models


class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __lt__(self, other):
        return self.name < other.name


class StudentGroup(models.Model):
    name = models.CharField("ime", max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    _students = models.TextField(
        "učenci", blank=True, help_text="V vsako vrstico vnesite ime enega učenca."
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("students:view_group", kwargs={"group_id": self.id})

    @property
    def students(self):
        return sorted(
            Student(id, name.strip())
            for id, name in enumerate(self._students.splitlines())
        )
