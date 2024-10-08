# Generated by Django 4.2.15 on 2024-08-24 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Machine",
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
                ("name", models.CharField(blank=True, max_length=300, null=True)),
                (
                    "type",
                    models.CharField(
                        choices=[("ovalama", "Ovalama"), ("press", "Press")],
                        max_length=100,
                    ),
                ),
                (
                    "variation",
                    models.CharField(
                        choices=[("type1", "Type1"), ("type2", "Type2")], max_length=100
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Siparis",
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
                ("definition", models.CharField(max_length=1000)),
                ("description", models.TextField(max_length=10000)),
                ("amount", models.IntegerField(default=0)),
                ("deadline", models.DateField(blank=True, null=True)),
                ("isOEM", models.BooleanField(default=False)),
                ("isActive", models.BooleanField(default=False)),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("Isıl İşlem", "Isil Islem"),
                            ("Kaplama", "Kaplama"),
                            ("Ovalama", "Ovalama"),
                            ("Patch", "Patch"),
                            ("Planlama", "Planlama"),
                            ("Press", "Press"),
                            ("Sipariş Tamamlandı", "Siparis Tamamlandi"),
                        ],
                        default="Planlama",
                        max_length=300,
                    ),
                ),
                (
                    "material",
                    models.CharField(
                        choices=[
                            ("20MnB4", " 1"),
                            ("15B2", " 2"),
                            ("CQ15", " 3"),
                            ("SAE100GC", " 4"),
                            ("304Cu(Paslanmaz)", " 5"),
                            ("Direct Çezim", " 6"),
                            ("23MnB4", " 7"),
                        ],
                        default="20MnB4",
                        max_length=300,
                    ),
                ),
                (
                    "quality",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Karbonhidrasyon", "Karbonhidration"),
                            ("10.8", " 108"),
                            ("4.8", " 48"),
                            ("6.8", " 68"),
                            ("8.8", " 88"),
                        ],
                        default="",
                        max_length=300,
                        null=True,
                    ),
                ),
                (
                    "kaplama",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Çinko Kaplama", " 1"),
                            ("Çinko Nikel Şeffaf Kaplama", " 2"),
                            ("Nikel Kaplama", " 3"),
                            ("Çinko Nikel Siyah Kaplama", " 4"),
                            ("Çinko Siyah Kaplama", " 5"),
                            ("Janjan Kaplama", " 6"),
                            ("Geomet Kaplama", " 7"),
                            ("Sarı Kaplama", " 8"),
                        ],
                        default="",
                        max_length=300,
                        null=True,
                    ),
                ),
                (
                    "patch",
                    models.CharField(blank=True, default="", max_length=300, null=True),
                ),
                (
                    "materialNumber",
                    models.CharField(blank=True, default="", max_length=300, null=True),
                ),
                ("orderNumber", models.IntegerField(editable=False, unique=True)),
                (
                    "clientOrderNumber",
                    models.CharField(blank=True, default="", max_length=300, null=True),
                ),
                (
                    "company",
                    models.CharField(
                        blank=True, default="", max_length=1000, null=True
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SiparisFile",
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
                ("title", models.CharField(blank=True, max_length=1000, null=True)),
                ("file", models.FileField(upload_to="")),
                (
                    "siparis",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="Vidasan.siparis",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
