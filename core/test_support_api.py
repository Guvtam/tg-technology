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
