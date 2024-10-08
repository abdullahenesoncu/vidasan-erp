# Generated by Django 4.2.15 on 2024-08-27 18:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Vidasan", "0005_alter_machine_variation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="siparis",
            name="material",
            field=models.CharField(
                choices=[
                    ("20MnB4", " 1"),
                    ("15B2", " 2"),
                    ("CQ15", " 3"),
                    ("SAE100GC", " 4"),
                    ("304Cu(Paslanmaz)", " 5"),
                    ("Direct Çekim", " 6"),
                    ("23MnB4", " 7"),
                ],
                default="20MnB4",
                max_length=300,
            ),
        ),
    ]
