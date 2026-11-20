import json
import logging
from urllib.request import Request, urlopen

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

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


def notify_contact_whatsapp(contact_id):
    config = settings.CONTACT_WHATSAPP
    if not all(config.values()):
        return

    payload = {
        "messaging_product": "whatsapp",
        "to": config["recipient"],
        "type": "template",
        "template": {
            "name": config["template"],
            "language": {"code": config["language"]},
            "components": [{
                "type": "body",
                "parameters": [{"type": "text", "text": str(contact_id)}],
            }],
        },
    }
    request = Request(
        f"https://graph.facebook.com/{config['version']}/{config['phone_id']}/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {config['token']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=5) as response:
            if not json.load(response).get("messages"):
                logger.error("WhatsApp no confirmó el aviso de la consulta %s", contact_id)
    except (OSError, ValueError) as exc:
        logger.error("Falló el aviso de WhatsApp para la consulta %s (%s)", contact_id, type(exc).__name__)


def home(request):
    if request.method == "POST":
        form = ContactRequestForm(request.POST)
        wants_json = request.headers.get("Accept") == "application/json"

        if form.is_valid():
            contact = form.save()
            transaction.on_commit(lambda: notify_contact_request(contact.pk), robust=True)
            transaction.on_commit(lambda: notify_contact_whatsapp(contact.pk), robust=True)

            if wants_json:
                return JsonResponse({"saved": True}, status=201)

            messages.success(
                request,
                (
                    "Gracias por contarnos sobre tu proyecto. Revisaremos tu solicitud "
                    "y te contactaremos para conversar sobre los próximos pasos."
                ),
                extra_tags="contact-confirmation",
            )

            return redirect(f"{reverse('core:home')}#inicio")
        if wants_json:
            return JsonResponse({"errors": form.errors.get_json_data()}, status=422)
    else:
        form = ContactRequestForm()

    return render(
        request,
        "core/home.html",
        {
            "contact_form": form,
        },
    )
