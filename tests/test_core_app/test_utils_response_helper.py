"""Module for testing the response helper"""

from src.apps.core.utilities.response_utils import ResponseHandler
from tests.fixtures.responses import (ERROR_RESPONSE, ERROR_RESPONSE_WMESSAGE,
                                      SUCCESS_RESPONSE,
                                      SUCCESS_RESPONSE_WMESSAGE)


class TestResponseHandler:
    """Tests the Response Handler"""

    def test_right_response_is_returned_for_errors_without_message_succeeds(
            self):
        """Test that the right response is return for errors without message"""
        response = ResponseHandler.response({'email': 'invalid'},
                                            status='error')

        assert response == ERROR_RESPONSE

    def test_right_response_is_returned_for_errors_with_message_succeeds(self):
        """Test that the right response is return for errors with message"""
        response = ResponseHandler.response({'email': 'invalid'},
                                            key='USR_O3',
                                            status='error')

        assert response == ERROR_RESPONSE_WMESSAGE

    def test_right_response_is_returned_for_success_without_message_succeeds(
            self):
        """Test that the right response is return for success without message"""
        response = ResponseHandler.response({'token': 'jwt_token'})

        assert response == SUCCESS_RESPONSE

    def test_right_response_is_returned_for_success_with_message_succeeds(
            self):
        """Test that the right response is return for success with message"""

        response = ResponseHandler.response({'token': 'jwt_token'},
                                            key='REGISTER')

        assert response == SUCCESS_RESPONSE_WMESSAGE
