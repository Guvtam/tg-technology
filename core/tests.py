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

        self.assertRedirects(response, reverse("core:home"), fetch_redirect_response=False)
        contact = ContactRequest.objects.get()
        self.assertEqual(contact.email, self.data["email"])
        self.assertEqual(len(callbacks), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["equipo@example.com"])
        self.assertIn(f"#{contact.pk}", mail.outbox[0].subject)
        self.assertNotIn(contact.email, mail.outbox[0].body)

    def test_mail_failure_leaves_contact_saved(self):
        with patch("core.views.send_mail", side_effect=OSError("SMTP unavailable")):
            with self.assertLogs("core.views", level="ERROR"):
                with self.captureOnCommitCallbacks(execute=True):
                    response = self.client.post(reverse("core:home"), self.data)

        self.assertRedirects(response, reverse("core:home"), fetch_redirect_response=False)
        self.assertTrue(ContactRequest.objects.filter(email=self.data["email"]).exists())

    def test_invalid_submission_does_not_save_or_notify(self):
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.post(reverse("core:home"), {**self.data, "email": "invalido"})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(ContactRequest.objects.exists())
        self.assertFalse(callbacks)
        self.assertFalse(mail.outbox)
