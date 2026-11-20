import json
from unittest.mock import patch
from uuid import uuid4

from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from core.support_api import SupportAPIError, registrar_ticket


class SupportAPITests(SimpleTestCase):
    @override_settings(TG_SUPPORT_API_URL="http://localhost:8001/soporte/api/tickets/", TG_SUPPORT_API_TOKEN="test-secret")
    @patch("core.support_api.urlopen")
    def test_sends_ticket_to_management(self, mock_urlopen):
        mock_urlopen.return_value.__enter__.return_value.read.return_value = b'{"codigo":"TCK-2026-00001"}'
        codigo = registrar_ticket({"referencia": str(uuid4()), "nombre": "Prueba", "correo": "a@example.com", "titulo": "Error", "descripcion": "No funciona"})
        self.assertEqual(codigo, "TCK-2026-00001")
        request = mock_urlopen.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer test-secret")
        self.assertEqual(request.get_method(), "POST")

    @override_settings(TG_SUPPORT_API_URL="http://example.com/soporte/api/tickets/", TG_SUPPORT_API_TOKEN="test-secret")
    def test_rejects_unencrypted_remote_endpoint(self):
        with self.assertRaises(SupportAPIError):
            registrar_ticket({})

    @override_settings(TG_SUPPORT_API_URL="", TG_SUPPORT_API_TOKEN="")
    def test_rejects_missing_configuration(self):
        with self.assertRaises(SupportAPIError):
            registrar_ticket({})


class SupportFormFlowTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("core:soporte")
        self.data = {
            "referencia": str(uuid4()), "nombre": "Ana Prueba",
            "correo": "ana@example.com", "categoria": "incidente", "impacto": "alto", "titulo": "Problema de acceso",
            "descripcion": "No puedo ingresar al sistema.",
        }

    @patch("core.views.registrar_ticket", return_value="TCK-2026-00001")
    def test_success_displays_ticket_code(self, registrar):
        response = self.client.post(self.url, self.data)
        self.assertRedirects(response, self.url)
        page = self.client.get(self.url)
        self.assertContains(page, "TCK-2026-00001")
        registrar.assert_called_once()

    @patch("core.views.registrar_ticket", side_effect=SupportAPIError("cliente_no_reconocido"))
    def test_unknown_customer_shows_field_error(self, registrar):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No encontramos un cliente activo")
        registrar.assert_called_once()

    @patch("core.views.registrar_ticket", side_effect=SupportAPIError())
    def test_network_failure_keeps_reference_for_retry(self, registrar):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No pudimos confirmar el ticket")
        self.assertContains(response, self.data["referencia"])
        registrar.assert_called_once()
