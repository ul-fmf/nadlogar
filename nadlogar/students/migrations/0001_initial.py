# Generated by Django 3.0.7 on 2020-12-01 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='students.StudentGroup')),
            ],
            options={
                'ordering': ['group', 'name'],
                'default_related_name': 'students',
            },
        ),
    ]