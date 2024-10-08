# Generated by Django 4.2.15 on 2024-08-20 17:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LogEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("level", models.CharField(max_length=50)),
                ("message", models.TextField()),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "logger_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("file_name", models.CharField(blank=True, max_length=255, null=True)),
                ("line_number", models.IntegerField(blank=True, null=True)),
                (
                    "function_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
