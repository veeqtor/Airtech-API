"""Module to handle all responses"""

from src.apps.core.utilities.messages import ERRORS, MESSAGES


class ResponseHandler(object):
    """
    Class that handles all API responses.
    """

    @staticmethod
    def response(data, key=None, status='success') -> dict:
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
