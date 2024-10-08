# Generated by Django 4.2.15 on 2024-08-20 19:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Authentication", "0004_alter_user_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(default="NULL", max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("Admin", "Admin"),
                    ("Depo", "Depo"),
                    ("Kalite kontrol", "Kalite Kontrol"),
                    ("Planlama", "Planlama"),
                    ("Satış/Pazarlama", "Satis Pazarlama"),
                ],
                default="Depo",
                max_length=100,
            ),
        ),
    ]
