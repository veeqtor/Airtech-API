"""Views"""

from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.response import Response

from src.apps.core.utilities.response_utils import ResponseHandler


def home(request):
    """Home"""

    return render(request, 'home.html')


class BaseModelViewSet(viewsets.ModelViewSet):
    """Base model view set"""

    http_method_names = ['get', 'post', 'head', 'patch']

    class Meta:
        """Meta"""
        abstract = True

    def get_object(self):
        """
        Get object from pk
        """
        query_set = self.get_queryset()
        obj = generics.get_object_or_404(query_set, **self.kwargs)
        return obj

    def list(self, request, *args, **kwargs):
        """
        Base List method
        """

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        res = ResponseHandler.response(serializer.data)
        return Response(res)

    def create(self, request, *args, **kwargs):
        """
        Base Add.
        """
        key = kwargs.get('key')

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            res = ResponseHandler.response(serializer.data, key=key)
            return Response(res,
                            status=status.HTTP_201_CREATED,
                            headers=headers)

        error = ResponseHandler.response(serializer.errors,
                                         key='USR_O3',
                                         status='error')
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Base retrieve method.
		"""

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        res = ResponseHandler.response(serializer.data)
        return Response(res)

    def partial_update(self, request, *args, **kwargs):
        """
        Base partial update.
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
