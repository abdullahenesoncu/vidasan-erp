# Generated by Django 4.2.15 on 2024-08-27 18:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Vidasan", "0007_alter_machine_type_alter_machine_variation"),
    ]

    operations = [
        migrations.AddField(
            model_name="siparis",
            name="orderDate",
            field=models.DateField(blank=True, null=True),
        ),
    ]
