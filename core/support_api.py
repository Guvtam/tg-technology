"""Client for the private TG Management support API."""
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings


class SupportAPIError(Exception):
    def __init__(self, code="servicio_no_disponible"):
        self.code = code
        super().__init__(code)


def registrar_ticket(datos):
    endpoint = getattr(settings, "TG_SUPPORT_API_URL", "").strip()
    token = getattr(settings, "TG_SUPPORT_API_TOKEN", "").strip()
    if not endpoint or not token:
        raise SupportAPIError()
    # HTTP only for explicitly local development. Remote servers must use HTTPS.
    if not (endpoint.startswith("https://") or endpoint.startswith("http://127.0.0.1:") or endpoint.startswith("http://localhost:")):
        raise SupportAPIError()
    request = Request(
        endpoint,
        data=json.dumps(datos, default=str).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=8) as response:
            resultado = json.load(response)
    except HTTPError as exc:
        if exc.code == 422:
            try:
                body = json.load(exc)
                if body.get("error") == "cliente_no_reconocido":
                    raise SupportAPIError("cliente_no_reconocido") from exc
            except (ValueError, AttributeError):
                pass
        raise SupportAPIError() from exc
    except (URLError, OSError, ValueError) as exc:
        raise SupportAPIError() from exc
    codigo = resultado.get("codigo") if isinstance(resultado, dict) else None
    if not isinstance(codigo, str) or not codigo:
        raise SupportAPIError()
    return codigo
