"""Module to handle all responses"""

from rest_framework.serializers import ValidationError
from rest_framework import status

from src.apps.core.utilities.messages import ERRORS, MESSAGES


class ResponseHandler(object):
    """
    Class that handles all API responses.
    """

    @classmethod
    def response(cls, data, key=None, status='success') -> dict:
        """
        Response helper for response messages.
        Args:
            data (dict or list): Data to return to user
            key (str): Message key
            status (str): Status of the response

        Returns:
            dict: The response dict
        """

        if key is None and status == 'error':
            return {'status': 'error', 'errors': data}
        elif key is not None and status == 'error':
            return {
                'status': 'error',
                'user_message': ERRORS[key],
                'errors': data
            }

        if key is None:
            return {'status': 'success', 'data': data}
        return {
            'status': 'success',
            'user_message': MESSAGES[key],
            'data': data
        }

    @classmethod
    def raise_error(cls, data):
        """
        Helper to raise validation errors.
        Args:
            data (dict or list): Data to return to user:

        Raises:
            JSON: The error response
        """

        error_message = cls.response(data, key='USR_O3', status='error')
        exception = ValidationError(error_message)
        exception.status_code = status.HTTP_400_BAD_REQUEST
        raise exception
