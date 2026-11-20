import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import ContactRequestForm


logger = logging.getLogger(__name__)


def notify_contact_request(contact_id):
    try:
        sent = send_mail(
            f"Nueva consulta TG Technology #{contact_id}",
            f"Se recibió la consulta #{contact_id}. Puedes revisarla en el panel de administración.",
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_NOTIFICATION_EMAIL],
        )
        if sent != 1:
            logger.error("No se envió el aviso de la consulta %s", contact_id)
    except Exception:
        logger.exception("Falló el envío del aviso de la consulta %s", contact_id)


def home(request):
    if request.method == "POST":
        form = ContactRequestForm(request.POST)

        if form.is_valid():
            contact = form.save()
            transaction.on_commit(lambda: notify_contact_request(contact.pk))

            messages.success(
                request,
                (
                    "Tu solicitud fue enviada correctamente. "
                    "Me pondré en contacto contigo a la brevedad."
                ),
            )

            return redirect("core:home")
    else:
        form = ContactRequestForm()

    return render(
        request,
        "core/home.html",
        {
            "contact_form": form,
        },
    )
