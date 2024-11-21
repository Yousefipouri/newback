"""
WSGI config for final_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""



import os
import sys

sys.path.append('/home/fatemehysf/newback')
os.environ['DJANGO_SETTINGS_MODULE'] = 'final_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
