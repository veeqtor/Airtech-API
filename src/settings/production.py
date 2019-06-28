""" Django production settings for airtech project."""

from os import environ
from . import *  # noqa: F403, F401

ENV = ('production', 'prod', 'Heroku', 'HEROKU', 'PROD', 'PRODUCTION')

HOST_ENV = environ.get('HOST_ENV')

if HOST_ENV in ENV:

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False
