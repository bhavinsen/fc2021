# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_email.settings')

application = get_wsgi_application()

# from whitenoise.django import DjangoWhiteNoise
# application = DjangoWhiteNoise(application)
