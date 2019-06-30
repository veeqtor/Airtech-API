"""Django test settings for airtech project"""

from os import environ  # noqa: F403, F401
from . import *  # noqa: F403, F401

LOGGING = {}
DEBUG = False
# Celery related
CELERY_ALWAYS_EAGER = True
