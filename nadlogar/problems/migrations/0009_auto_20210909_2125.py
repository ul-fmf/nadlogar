# Generated by Django 3.2.3 on 2021-09-09 19:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0008_auto_20210828_1305"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeliteljVeckratnik",
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
                    "minimalna_vrednost",
                    models.PositiveSmallIntegerField(
                        help_text="Najmanjša možna vrednost katerega izmed števil",
                        verbose_name="minimalna vrednost",
                    ),
                ),
                (
                    "maksimalna_vrednost",
                    models.PositiveSmallIntegerField(
                        help_text="Največja možna vrednost katerega izmed števil",
                        verbose_name="maksimalna vrednost",
                    ),
                ),
                (
                    "maksimalni_prafaktor",
                    models.PositiveSmallIntegerField(
                        help_text="Zgornja meja za prafaktorje števil",
                        verbose_name="maksimalni prafaktor",
                    ),
                ),
            ],
            options={
                "verbose_name": "največji skupni delitelj in najmanjši skupni večkratnik",
            },
            bases=("problems.problem",),
        ),
        migrations.CreateModel(
            name="EvklidovAlgoritem",
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
                "verbose_name": "evklidov algoritem",
            },
            bases=("problems.problem",),
        ),
        migrations.AlterField(
            model_name="potencavecclenika",
            name="najmanj_clenov",
            field=models.PositiveSmallIntegerField(
                help_text="Najmanjše možno število členov v veččleniku.",
                verbose_name="najmanj členov",
            ),
        ),
        migrations.AlterField(
            model_name="potencavecclenika",
            name="najvec_clenov",
            field=models.PositiveSmallIntegerField(
                help_text="Največje možno število členov v veččleniku.",
                verbose_name="največ členov",
            ),
        ),
    ]
