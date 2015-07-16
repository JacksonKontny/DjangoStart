"""
WSGI config for scrape_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from settings.base import PROJECT_NAME

os.environ.setdefault("DJANGO_SETTINGS_MODULE", '%s.settings.base' % PROJECT_NAME)

application = get_wsgi_application()
