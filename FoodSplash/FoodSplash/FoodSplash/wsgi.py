"""
WSGI config for BV_Server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
from . import settings


if settings.PRODUCTION:
    from django.core.wsgi import get_wsgi_application
    from djangae.wsgi import DjangaeApplication

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FoodSplash.settings")
    application = DjangaeApplication(get_wsgi_application())

else:
    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FoodSplash.settings")
    application = get_wsgi_application()
