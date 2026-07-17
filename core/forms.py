from django import forms

from .models import ContactRequest


class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest

        fields = [
            "name",
            "company",
            "email",
            "phone",
            "service",
            "budget",
            "message",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Tu nombre",
                    "autocomplete": "name",
                }
            ),
            "company": forms.TextInput(
                attrs={
                    "placeholder": "Nombre de tu empresa",
                    "autocomplete": "organization",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "correo@empresa.cl",
                    "autocomplete": "email",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "+56 9 1234 5678",
                    "autocomplete": "tel",
                }
            ),
            "service": forms.Select(),
            "budget": forms.Select(
                choices=[
                    ("", "Selecciona un rango"),
                    ("menos-300", "Menos de $300.000"),
                    ("300-600", "$300.000 a $600.000"),
                    ("600-1000", "$600.000 a $1.000.000"),
                    ("mas-1000", "Más de $1.000.000"),
                    ("evaluar", "Necesito orientación"),
                ]
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Cuéntame qué necesitas, qué problema deseas "
                        "resolver y qué resultado esperas obtener."
                    ),
                    "rows": 6,
                }
            ),
        }