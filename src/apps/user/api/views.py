"""API View module for users"""

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from src.apps.user.api.serializer import UserSerializer
from src.apps.core.utilities import random_token
from src.apps.core.utilities.response_utils import ResponseHandler

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserRegister(generics.CreateAPIView):
    """Class representing the view for creating a new user"""

    serializer_class = UserSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs) -> object:
        """Creates a new user.

        Args:
            request (object): Request object
            *args:
            **kwargs:
        Returns:
            JSON
        """
        serializer = UserSerializer(data=request.data)
        verification_token = random_token.generate_verification_token(10)
        if serializer.is_valid():
            serializer.validated_data[
                'verification_token'] = verification_token
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            payload = jwt_payload_handler(serializer.data)
            token = jwt_encode_handler(payload)
            res = ResponseHandler.response({'token': token}, key='REGISTER')
            return Response(res,
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        error = ResponseHandler.response(serializer.errors,
                                         key='USR_O3',
                                         status='error')
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
