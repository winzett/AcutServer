"""
WSGI config for acut project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os,sys
from django.core.wsgi import get_wsgi_application
os.environ["DJANGO_SETTINGS_MODULE"] = "acut.settings"
os.environ["SENDGRID_API_KEY"] = "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"
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acut.settings")
path=os.path.abspath(__file__+'/../..')
if path not in sys.path:
  sys.path.append(path)
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acut.settings")


application = get_wsgi_application()
