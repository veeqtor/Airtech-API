"""API View module for flights"""

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status  # noqa: F401
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from src.apps.core.utilities.response_utils import ResponseHandler
from src.apps.flight.models import (Plane, Flight)  # noqa: F401
from src.apps.flight.api.serializers import (
    PlaneSerializer,  # noqa: F401
    AvailableSeatsSerializer,
    FlightWithPlaneSerializer,
    FlightSerializer)


class FlightViewSet(viewsets.ModelViewSet):
    """View set for Flight."""

    serializer_class = FlightSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        """
        List of flights
        """

        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        res = ResponseHandler.response(serializer.data)
        return Response(res)

    def create(self, request, *args, **kwargs):
        """
        Add a flight.
        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            res = ResponseHandler.response(serializer.data, key='FLIGHT')
            return Response(res,
                            status=status.HTTP_201_CREATED,
                            headers=headers)

        error = ResponseHandler.response(serializer.errors,
                                         key='USR_O3',
                                         status='error')
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Get a particular flight.
        """

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        res = ResponseHandler.response(serializer.data)
        return Response(res)

    def partial_update(self, request, *args, **kwargs):
        """
        Update flight.
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

    @action(detail=True)
    def available_seats(self, request, *args, **kwargs):  # noqa: F401
        """
        Get available seats for a particular flight.
        """

        query_type = request.query_params.get('type', None)

        if query_type:
            instance = self.get_object().plane.seats.filter(booked=False,
                                                            reserved=False,
                                                            type=query_type,
                                                            deleted=False)
        else:
            instance = self.get_object().plane.seats.filter(booked=False,
                                                            reserved=False,
                                                            deleted=False)
        serializer = AvailableSeatsSerializer(instance, many=True)
        res = ResponseHandler.response(serializer.data)
        return Response(res)

    def get_queryset(self):
        """
        Default get query set
        """

        qs = Flight.objects.filter(plane__grounded=False,
                                   deleted=False)\
            .select_related('plane').prefetch_related('plane__seats')

        return qs

    def get_object(self):
        """
        Get object from pk
        """
        query_set = self.get_queryset()
        obj = generics.get_object_or_404(query_set, **self.kwargs)
        return obj

    def get_serializer_class(self):
        """
        Custom serializer
        """

        if self.action not in ('create', 'partial_update'):
            self.serializer_class = FlightWithPlaneSerializer

        return super(self.__class__, self).get_serializer_class()

    def get_permissions(self):
        """
        Custom permission
        """

        if self.action in ('list', 'retrieve', 'available_seats'):
            self.permission_classes = [IsAuthenticated]

        return super(self.__class__, self).get_permissions()


class PlaneView(viewsets.ModelViewSet):
    """
    View set for Plane.
    """

    serializer_class = PlaneSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        """
        List of plane
        """

        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        res = ResponseHandler.response(serializer.data)
        return Response(res)

    def create(self, request, *args, **kwargs):
        """
        Add a plane.
        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            res = ResponseHandler.response(serializer.data, key='PLANE')
            return Response(res,
                            status=status.HTTP_201_CREATED,
                            headers=headers)

        error = ResponseHandler.response(serializer.errors,
                                         key='USR_O3',
                                         status='error')
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Get a particular flight.
        """

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        res = ResponseHandler.response(serializer.data)
        return Response(res)

    def partial_update(self, request, *args, **kwargs):
        """
        Update flight.
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

    def get_queryset(self):
        """
        Default get query set
        """

        return Plane.objects.filter(grounded=False, deleted=False)

    def get_object(self):
        """
        Get object from pk
        """
        query_set = self.get_queryset()
        obj = generics.get_object_or_404(query_set, **self.kwargs)
        return obj

    def get_permissions(self):
        """
        Custom permission
        """

        if self.action in ('list', 'retrieve'):
            self.permission_classes = [IsAuthenticated]

        return super(self.__class__, self).get_permissions()
