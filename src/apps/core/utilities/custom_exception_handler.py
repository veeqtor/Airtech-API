"""Custom error handler module"""

from rest_framework import status
from rest_framework.views import exception_handler
from src.apps.core.utilities.messages import ERRORS


def custom_exception_handler(exc, context):
    """Custom exception handler"""

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response and response.status_code == status.HTTP_404_NOT_FOUND:
        response.data = {'status': 'error', 'user_message': ERRORS['USR_09']}

    elif response and response.status_code == status.HTTP_401_UNAUTHORIZED:

        response.data = {
            'status': 'error',
            'user_message': response.data.get('detail')
        }

    return response
