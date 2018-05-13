#!/usr/bin/env python

"""
WSGI config for cashflow project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys

from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cashflow.settings")

application = get_wsgi_application()


execute_from_command_line(sys.argv)
