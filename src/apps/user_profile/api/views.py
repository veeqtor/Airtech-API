"""API View module for users"""

from rest_framework import generics, views
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.apps.core.views import BaseModelViewSet
from src.apps.core.utilities.response_utils import ResponseHandler
from src.apps.user_profile.api.serializers import (UserProfileSerializer,
                                                   PassportSerializer)
from src.tasks.file_uploads import FileUpload


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

        error = ResponseHandler.response(serializer.errors,
                                         key='USR_O3',
                                         status='error')
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """
        Default query set.
        """

        user = self.request.user
        return user.user_profile


class PassportViewSet(BaseModelViewSet):
    """
    View set for Passport.
    """

    serializer_class = PassportSerializer
    permission_classes = [IsAuthenticated]
    BaseModelViewSet.http_method_names += ['delete']

    def create(self, request, *args, **kwargs):
        """
        Add passport.
        """

        return super(self.__class__, self).create(request, key='PASSPORT')

    def get_queryset(self):
        """
        Default query set
        """

        user = self.request.user
        return user.user_profile.passports.filter(deleted=False)


class ImageUpload(views.APIView):
    """Passport photograph upload."""

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def put(self, request, *args, **kwargs):
        """Put method to upload passport."""

        file_obj = request.FILES.get('photo', None)

        user_profile_qs = self.get_queryset()

        FileUpload.image(file_obj, user_profile_qs)

        response = ResponseHandler.response(data=[], key='PHOTO_UPLOAD')
        return Response(response)

    def get_queryset(self):
        """
        Default query set.
        """

        user = self.request.user
        return user.user_profile
