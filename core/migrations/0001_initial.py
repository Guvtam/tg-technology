from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Nombre")),
                ("company", models.CharField(blank=True, max_length=150, verbose_name="Empresa")),
                ("email", models.EmailField(max_length=254, verbose_name="Correo electrónico")),
                ("phone", models.CharField(blank=True, max_length=30, verbose_name="Teléfono")),
                ("service", models.CharField(
                    choices=[
                        ("web", "Página web"),
                        ("system", "Sistema web"),
                        ("data", "Análisis de datos"),
                        ("ecommerce", "Tienda online"),
                        ("other", "Otra solución"),
                    ],
                    max_length=30,
                    verbose_name="Servicio",
                )),
                ("budget", models.CharField(blank=True, max_length=80, verbose_name="Presupuesto aproximado")),
                ("message", models.TextField(verbose_name="Descripción del proyecto")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de solicitud")),
                ("is_contacted", models.BooleanField(default=False, verbose_name="Contactado")),
            ],
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Solicitud de contacto",
                "verbose_name_plural": "Solicitudes de contacto",
            },
        ),
    ]
