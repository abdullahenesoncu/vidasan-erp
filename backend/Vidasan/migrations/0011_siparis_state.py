# Generated by Django 4.2.15 on 2024-08-29 14:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Vidasan", "0010_alter_siparis_ambalajstate_alter_siparis_byckstate_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="siparis",
            name="state",
            field=models.CharField(
                choices=[
                    ("İmalat", "Imalat"),
                    ("Planlama", "Planlama"),
                    ("Sipariş Tamamlandı", "Siparis Tamamlandi"),
                ],
                default="Planlama",
                max_length=100,
            ),
        ),
    ]
