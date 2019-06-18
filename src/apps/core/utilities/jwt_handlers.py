"""Module for jwt handling"""

from datetime import datetime
from rest_framework_jwt.settings import api_settings

from src.apps.core.utilities.response_utils import ResponseHandler


def jwt_payload_handler(user):
    """JWT payload handler"""

    payload = {
        'id': user.get('id'),
        'email': user.get('email'),
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload


def jwt_response_payload_handler(token, user=None, request=None):
    """Returns the response data for both the login and refresh views."""

    return ResponseHandler.response({'token': token}, key='LOGIN')
