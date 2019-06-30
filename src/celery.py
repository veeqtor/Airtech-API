"""Celery config"""

import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings.production')
celery_app = Celery('src')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
settings.DEBUG = True
celery_app.config_from_object('django.conf:settings')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
