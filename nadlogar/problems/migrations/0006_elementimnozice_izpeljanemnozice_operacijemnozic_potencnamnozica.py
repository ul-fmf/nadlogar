# Generated by Django 3.2.3 on 2021-08-02 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0005_auto_20210728_1109"),
    ]

    operations = [
        migrations.CreateModel(
            name="ElementiMnozice",
            fields=[
                (
                    "problem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="problems.problem",
                    ),
                ),
                (
                    "linearna_kombinacija",
                    models.BooleanField(
                        choices=[(True, "Da"), (False, "Ne")],
                        help_text="Ali naj naloga vsebuje linearno kombinacijo?",
                        verbose_name="linearna kombinacija",
                    ),
                ),
            ],
            options={
                "verbose_name": "elementi množice",
            },
            bases=("problems.problem",),
        ),
        migrations.CreateModel(
            name="IzpeljaneMnozice",
            fields=[
                (
                    "problem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="problems.problem",
                    ),
                ),
            ],
            options={
                "verbose_name": "izpeljane množice",
            },
            bases=("problems.problem",),
        ),
        migrations.CreateModel(
            name="OperacijeMnozic",
            fields=[
                (
                    "problem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="problems.problem",
                    ),
                ),
            ],
            options={
                "verbose_name": "operacije z množicami",
            },
            bases=("problems.problem",),
        ),
        migrations.CreateModel(
            name="PotencnaMnozica",
            fields=[
                (
                    "problem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="problems.problem",
                    ),
                ),
            ],
            options={
                "verbose_name": "potenčna množica",
            },
            bases=("problems.problem",),
        ),
    ]
