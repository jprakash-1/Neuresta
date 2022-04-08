"""
WSGI config for wad_nst project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad_nst.settings')

application = get_wsgi_application()

CRISPY_TEMPLATE_PACK = 'bootstrap4'