""" Django production settings for airtech project."""

from os import environ
from . import *  # noqa: F403, F401

ENV = ('production', 'prod', 'Heroku', 'HEROKU', 'PROD', 'PRODUCTION')

HOST_ENV = environ.get('HOST_ENV')

if HOST_ENV in ENV:

    #  Add configuration for static files storage using whitenoise
    STATICFILES_STORAGE = 'whitenoise.storage.' \
                          'CompressedManifestStaticFilesStorage'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False
    SSL_ENABLED = True

    CACHES = {
        "default": {
            "BACKEND": "redis_cache.RedisCache",
            "LOCATION": os.environ.get('REDIS_URL'),
        }
    }

    import django_heroku

    # Activate Django-Heroku.
    django_heroku.settings(locals())
