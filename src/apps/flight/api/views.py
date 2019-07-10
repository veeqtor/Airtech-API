"""API View module for flights"""
from django.db import connection
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from src.apps.core.views import BaseModelViewSet
from src.apps.core.utilities.response_utils import ResponseHandler
from src.apps.core.utilities.validations import date_validator
from src.apps.flight.models import (Plane, Flight)  # noqa: F401
from src.apps.flight.api.serializers import (
    PlaneSerializer,  # noqa: F401
    AvailableSeatsSerializer,
    FlightWithPlaneSerializer,
    FlightSerializer,
    StatusSerializer)


class FlightViewSet(BaseModelViewSet):
    """View set for Flight."""

    serializer_class = FlightSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        """
        Add a flight.
        """
        return super(self.__class__, self).create(request, key='FLIGHT')

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

    @action(detail=True)
    def status(self, request, *args, **kwargs):  # noqa: F401
        """
        Get status seats for a particular flight.
        """
        instance = self.get_object()
        serializer = StatusSerializer(instance)
        res = ResponseHandler.response(serializer.data)
        return Response(res)

    def reservation_count_query(self, pk, date):
        """query to get the reservation count."""

        query = "SELECT COUNT(*) AS reservation_count " \
                "FROM bo_reservations WHERE bo_reservations.flight_id = " \
                "(SELECT fl_flights.id FROM fl_flights " \
                "INNER JOIN fl_planes " \
                "ON (fl_flights.plane_id = fl_planes.id) " \
                "WHERE (fl_flights.deleted = false " \
                "AND fl_planes.grounded = false " \
                "AND fl_flights.id = %s " \
                "AND fl_flights.date = %s));"

        with connection.cursor() as cursor:
            cursor.execute(query, [pk, str(date)])
            row = cursor.fetchone()

        return row

    @action(detail=True)
    def reservations(self, request, *args, **kwargs):  # noqa: F401
        """
        Get the total count of the reservations
        """
        date = request.query_params.get('date', None)
        date_obj = date_validator(date)
        pk = kwargs['pk']

        count = self.reservation_count_query(pk, date_obj)

        res = ResponseHandler.response({'reservations': count[0]})

        return Response(res)

    def get_queryset(self):
        """
        Default get query set
        """

        qs = Flight.objects.filter(plane__grounded=False,
                                   deleted=False) \
            .select_related('plane').prefetch_related('plane__seats')

        return qs

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

        actions = ('list', 'retrieve', 'available_seats', 'status')

        if self.action in actions:
            self.permission_classes = [IsAuthenticated]

        return super(self.__class__, self).get_permissions()


class PlaneView(BaseModelViewSet):
    """
    View set for Plane.
    """

    serializer_class = PlaneSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        """
        Add a plane.
        """
        return super(self.__class__, self).create(request, key='FLIGHT')

    def get_queryset(self):
        """
        Default get query set
        """

        return Plane.objects.filter(grounded=False, deleted=False)

    def get_permissions(self):
        """
        Custom permission
        """

        if self.action in ('list', 'retrieve'):
            self.permission_classes = [IsAuthenticated]

        return super(self.__class__, self).get_permissions()
