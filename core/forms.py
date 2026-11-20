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
                    "placeholder": "Ej. Taller Los Andes",
                    "autocomplete": "organization",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "nombre@ejemplo.cl",
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