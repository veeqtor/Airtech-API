"""Module to hold fixtures for the response util"""

from src.apps.core.utilities.messages import ERRORS, MESSAGES

ERROR_RESPONSE = {'status': 'error', 'errors': {'email': 'invalid'}}

ERROR_RESPONSE_WMESSAGE = {
    'status': 'error',
    'user_message': ERRORS['USR_O3'],
    'errors': {
        'email': 'invalid'
    }
}

SUCCESS_RESPONSE = {'status': 'success', 'data': {'token': 'jwt_token'}}

SUCCESS_RESPONSE_WMESSAGE = {
    'status': 'success',
    'user_message': MESSAGES['REGISTER'],
    'data': {
        'token': 'jwt_token'
    }
}
