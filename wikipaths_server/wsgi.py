"""
WSGI config for wikipaths_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wikipaths_server.settings")

#application = get_wsgi_application()

#If production env
if "BLUEMIX_REGION" in os.environ:
    from dj_static import Cling
    #Serve static files with gunicorn
    application = Cling(get_wsgi_application())
else: #if non production env
    application = get_wsgi_application()
