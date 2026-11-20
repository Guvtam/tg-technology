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

class SoporteWebForm(forms.Form):
    referencia = forms.UUIDField(widget=forms.HiddenInput)
    nombre = forms.CharField(label="Nombre", max_length=120)
    correo = forms.EmailField(label="Correo electrónico")
    titulo = forms.CharField(label="Asunto", max_length=200)
    descripcion = forms.CharField(label="Describe el problema", max_length=5000, widget=forms.Textarea(attrs={"rows": 5}))
