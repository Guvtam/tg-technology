# TG Technology

Sitio comercial en Django. Para instalar y comprobar el formulario con Python 3.12 o superior:

```sh
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py test core
```

Si una instalación existente ya tiene la tabla `core_contactrequest`, respalda la base y comprueba que la tabla coincide con la migración inicial. En ese caso, usa `python manage.py migrate --fake-initial` para registrar esa migración conservando los datos.

## Avisos de consultas

Configura estas variables en el entorno del servidor:

| Variable | Valor |
| --- | --- |
| `EMAIL_HOST` | Servidor SMTP del proveedor |
| `EMAIL_PORT` | Puerto del proveedor, por defecto 587 |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | Credenciales SMTP |
| `EMAIL_USE_TLS`, `EMAIL_USE_SSL` | Valores `true` o `false`. Por defecto usa STARTTLS. Para SSL implícito, activa SSL y desactiva TLS. |
| `DEFAULT_FROM_EMAIL` | Remitente autorizado por el proveedor |
| `CONTACT_NOTIFICATION_EMAIL` | Buzón receptor, por defecto `contacto@tg-technology.cl` |

Envía una consulta de prueba y verifica tanto el registro en el panel de administración como la llegada al buzón. Si SMTP falla, la consulta queda guardada y el error aparece en los registros de la aplicación. Revisa el panel mientras resuelves la incidencia. El envío fallido requiere seguimiento manual.

## Aviso opcional por WhatsApp

Configura `CONTACT_WHATSAPP_VERSION`, `CONTACT_WHATSAPP_PHONE_ID`,
`CONTACT_WHATSAPP_TOKEN`, `CONTACT_WHATSAPP_RECIPIENT` (número del negocio
en formato internacional), `CONTACT_WHATSAPP_TEMPLATE` y, si corresponde,
`CONTACT_WHATSAPP_LANGUAGE` (por defecto `es`). Usa una plantilla aprobada
por Meta con un parámetro de texto en el cuerpo para el número de solicitud.
Sin esta configuración, se omite el aviso de WhatsApp.

## Formulario de soporte en local

La ruta `/soporte/` registra tickets en TG Management mediante su comando
`registrar_soporte_web`. En Windows, coloca ambos proyectos en la misma
carpeta y usa el entorno `.venv` de Management. Si la ruta cambia, configura
`TG_SUPPORT_CRM_DIR`. Aplica primero las migraciones de Management.
