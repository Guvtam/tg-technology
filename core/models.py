from django.db import models

# Create your models here.
from django.db import models


class ContactRequest(models.Model):
    SERVICE_CHOICES = [
        ("web", "Página web"),
        ("system", "Sistema web"),
        ("data", "Análisis de datos"),
        ("ecommerce", "Tienda online"),
        ("other", "Otra solución"),
    ]

    name = models.CharField("Nombre", max_length=120)
    company = models.CharField(
        "Empresa",
        max_length=150,
        blank=True,
    )
    email = models.EmailField("Correo electrónico")
    phone = models.CharField(
        "Teléfono",
        max_length=30,
        blank=True,
    )
    service = models.CharField(
        "Servicio",
        max_length=30,
        choices=SERVICE_CHOICES,
    )
    budget = models.CharField(
        "Presupuesto aproximado",
        max_length=80,
        blank=True,
    )
    message = models.TextField("Descripción del proyecto")
    created_at = models.DateTimeField(
        "Fecha de solicitud",
        auto_now_add=True,
    )
    is_contacted = models.BooleanField(
        "Contactado",
        default=False,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Solicitud de contacto"
        verbose_name_plural = "Solicitudes de contacto"

    def __str__(self):
        return f"{self.name} - {self.get_service_display()}"