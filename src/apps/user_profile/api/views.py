"""API View module for users"""

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.apps.core.utilities.response_utils import ResponseHandler
from src.apps.user_profile.api.serializers import (UserProfileSerializer,
                                                   PassportSerializer)


class UserProfileUpdate(generics.RetrieveUpdateAPIView):
    """Class representing the view for getting and updating a user profile"""

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs) -> object:
        """
        Getting the profile of a logged in user.
        """
        instance = self.get_queryset()
        serializer = self.get_serializer(instance)
        response = ResponseHandler.response(serializer.data)
        return Response(response)

    def patch(self, request, *args, **kwargs) -> object:
        """
        Updates user profile.
        """

        instance = self.get_queryset()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            response = ResponseHandler.response(serializer.data)
            return Response(response)

        error = ResponseHandler.response(serializer.errors, status='error')
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """Default query set"""

        user = self.request.user
        return user.user_profile


class PassportViewSet(viewsets.ModelViewSet):
    """View set for Passport"""

    serializer_class = PassportSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        List all Passports for the logged in user.
        """
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        response = ResponseHandler.response(serializer.data)
        return Response(response)

    def create(self, request, *args, **kwargs):
        """
        Add passport.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            res = ResponseHandler.response(serializer.data, key='PASSPORT')
            return Response(res,
                            status=status.HTTP_201_CREATED,
                            headers=headers)

        error = ResponseHandler.response(serializer.errors,
                                         key='USR_O3',
                                         status='error')
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a passport.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = ResponseHandler.response(serializer.data)
        return Response(response)

    def partial_update(self, request, *args, **kwargs):
        """
        Update passport
        """

        query_set = self.get_object()
        serializer = self.get_serializer(query_set,
                                         data=request.data,
                                         partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            response = ResponseHandler.response(serializer.data)
            return Response(response)

        error = ResponseHandler.response(serializer.errors, status='error')
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        """
        Get object from pk
        """

        query_set = self.get_queryset()
        obj = generics.get_object_or_404(query_set, **self.kwargs)
        return obj

    def get_queryset(self):
        """
        Default query set
        """

        user = self.request.user
        return user.user_profile.passports.filter(deleted=False)
