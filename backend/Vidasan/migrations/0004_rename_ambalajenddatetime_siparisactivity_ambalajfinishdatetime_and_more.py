# Generated by Django 4.2.15 on 2024-08-24 22:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Vidasan", "0003_siparisactivity_ambalajenddatetime_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="siparisactivity",
            old_name="ambalajEndDateTime",
            new_name="ambalajFinishDateTime",
        ),
        migrations.RenameField(
            model_name="siparisactivity",
            old_name="byckEndDateTime",
            new_name="byckFinishDateTime",
        ),
        migrations.RenameField(
            model_name="siparisactivity",
            old_name="kaplamaEndDateTime",
            new_name="kaplamaFinishDateTime",
        ),
        migrations.RenameField(
            model_name="siparisactivity",
            old_name="ovalamaEndDateTime",
            new_name="ovalamaFinishDateTime",
        ),
        migrations.RenameField(
            model_name="siparisactivity",
            old_name="pressEndDateTime",
            new_name="pressFinishDateTime",
        ),
        migrations.RenameField(
            model_name="siparisactivity",
            old_name="sementasyonEndDateTime",
            new_name="sementasyonFinishDateTime",
        ),
    ]
