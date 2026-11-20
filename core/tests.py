from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ContactRequest


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    CONTACT_NOTIFICATION_EMAIL="equipo@example.com",
)
class ContactRequestTests(TestCase):
    data = {
        "name": "Cliente de prueba",
        "email": "cliente@example.com",
        "service": "web",
        "message": "Necesito un sitio corporativo.",
    }

    def test_valid_submission_saves_and_notifies_after_commit(self):
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.post(reverse("core:home"), self.data)

        self.assertRedirects(response, reverse("core:home") + "#inicio", fetch_redirect_response=False)
        page = self.client.get(reverse("core:home"))
        self.assertContains(page, "Solicitud recibida")
        self.assertContains(page, "<dialog", html=False)
        self.assertNotContains(self.client.get(reverse("core:home")), "contact-fallback")
        contact = ContactRequest.objects.get()
        self.assertEqual(contact.email, self.data["email"])
        self.assertEqual(len(callbacks), 2)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["equipo@example.com"])
        self.assertIn(f"#{contact.pk}", mail.outbox[0].subject)
        self.assertNotIn(contact.email, mail.outbox[0].body)

    def test_mail_failure_leaves_contact_saved(self):
        with patch("core.views.send_mail", side_effect=OSError("SMTP unavailable")):
            with self.assertLogs("core.views", level="ERROR"):
                with self.captureOnCommitCallbacks(execute=True):
                    response = self.client.post(reverse("core:home"), self.data)

        self.assertRedirects(response, reverse("core:home") + "#inicio", fetch_redirect_response=False)
        self.assertTrue(ContactRequest.objects.filter(email=self.data["email"]).exists())

    def test_invalid_submission_does_not_save_or_notify(self):
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.post(reverse("core:home"), {**self.data, "email": "invalido"})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(ContactRequest.objects.exists())
        self.assertFalse(callbacks)
        self.assertFalse(mail.outbox)


    @override_settings(CONTACT_WHATSAPP={
        "version": "v27.0",
        "phone_id": "123456",
        "token": "test-token",
        "recipient": "56912345678",
        "template": "nueva_consulta",
        "language": "es",
    })
    def test_whatsapp_notifies_business_without_lead_details(self):
        import json

        with patch("core.views.urlopen") as send:
            send.return_value.__enter__.return_value.read.return_value = b'{"messages":[{"id":"test"}]}'
            with self.captureOnCommitCallbacks(execute=True):
                self.client.post(reverse("core:home"), self.data)

        request = send.call_args.args[0]
        payload = json.loads(request.data)
        self.assertEqual(payload["to"], "56912345678")
        self.assertEqual(
            payload["template"]["components"][0]["parameters"][0]["text"],
            str(ContactRequest.objects.get().pk),
        )
        self.assertNotIn(self.data["email"], request.data.decode())


    def test_async_submission_returns_success_without_redirect(self):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse("core:home"), self.data, HTTP_ACCEPT="application/json"
            )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"saved": True})
        self.assertEqual(ContactRequest.objects.count(), 1)

    def test_async_invalid_submission_reports_field_errors(self):
        response = self.client.post(
            reverse("core:home"),
            {**self.data, "email": "invalido"},
            HTTP_ACCEPT="application/json",
        )

        self.assertEqual(response.status_code, 422)
        self.assertIn("email", response.json()["errors"])
        self.assertFalse(ContactRequest.objects.exists())
