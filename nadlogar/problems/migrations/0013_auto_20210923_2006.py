# Generated by Django 3.2.6 on 2021-09-23 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0012_auto_20210923_2005"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prostobesedilo",
            name="navodilo",
            field=models.TextField(
                default="",
                help_text="Poljubno besedilo navodila.",
                verbose_name="navodilo",
            ),
        ),
        migrations.AlterField(
            model_name="prostobesedilo",
            name="resitev",
            field=models.TextField(
                default="",
                help_text="Poljubno besedilo rešitve.",
                verbose_name="rešitev",
            ),
        ),
    ]
