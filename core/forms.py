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
    nombre = forms.CharField(label="Nombre completo", max_length=120, widget=forms.TextInput(attrs={"placeholder": "Ej. Ana González", "autocomplete": "name"}))
    correo = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={"placeholder": "correo@empresa.cl", "autocomplete": "email"}))
    categoria = forms.ChoiceField(label="Tipo de solicitud", choices=[("incidente", "Error o incidente"), ("solicitud_cambio", "Solicitud de cambio"), ("duda", "Consulta"), ("mantencion", "Mantención"), ("otro", "Otro")])
    impacto = forms.ChoiceField(label="Impacto del problema", choices=[("bajo", "Bajo: puedo seguir trabajando"), ("medio", "Medio: afecta algunas funciones"), ("alto", "Alto: no puedo utilizar el servicio")])
    titulo = forms.CharField(label="Asunto", max_length=200, widget=forms.TextInput(attrs={"placeholder": "Ej. No puedo ingresar a mi plataforma"}))
    descripcion = forms.CharField(label="Describe el problema", max_length=5000, widget=forms.Textarea(attrs={"rows": 6, "placeholder": "Describe el problema, cuándo comenzó y cómo podemos reproducirlo..."}))
