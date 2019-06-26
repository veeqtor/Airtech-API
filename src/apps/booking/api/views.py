"""Module for the bookings views."""
from datetime import timedelta, date
from django.conf import settings
from rest_framework import generics, status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from src.apps.core.utilities.response_utils import ResponseHandler
from src.apps.core.utilities.messages import MESSAGES
from src.apps.booking.models import (Reservation, Ticket)
from src.apps.flight.models import Flight
from src.apps.booking.api.serializers import (ReservationSerializer,
                                              TicketSerializer)


class ReservationsView(mixins.CreateModelMixin, mixins.ListModelMixin,
                       mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    View set for Reservations.
    """
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """Method to list reservations made."""

        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        res = ResponseHandler.response(serializer.data)
        return Response(res)

    def create(self, request, *args, **kwargs):
        """Method to create a ticket."""

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = request.data

            flight_qs = Flight\
                .objects.filter(pk=data['flight'],
                                plane__grounded=False,
                                plane__seats__type=data['type'],
                                plane__seats__seat_number=data['seat_number'],
                                plane__seats__reserved=False,
                                plane__seats__booked=False,
                                plane__seats__deleted=False)\
                .select_related('plane').prefetch_related('plane__seats')\
                .first()

            if flight_qs is not None:

                available_seat = flight_qs.plane.seats.get(
                    type=data['type'],
                    seat_number=data['seat_number'],
                    reserved=False,
                    booked=False,
                    deleted=False)

                reservation = {
                    'flight': flight_qs,
                    'type': available_seat.type,
                    'seat_number': available_seat.seat_number,
                    'made_by': request.user
                }

                reservation_saved = Reservation.objects.create(**reservation)

                if reservation_saved:
                    available_seat.reserved = True
                    available_seat.save()

                    res = ResponseHandler.response(
                        data=MESSAGES['RESERVED'].format(
                            available_seat.seat_number,
                            flight_qs.flight_number))

                    return Response(res)

            error = ResponseHandler.response({}, key='FLI_01', status='error')

            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        error = ResponseHandler.response(serializer.errors,
                                         key='USR_O3',
                                         status='error')
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """Method to edit a reservation."""

        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=True)
        today = date.today()
        flight_date = instance.flight.date

        # Check if the dates are with edit range
        if (flight_date -
                today) <= timedelta(days=settings.FLIGHT_EDIT_ALLOWANCE_DAYS):
            error = ResponseHandler.response({}, key='FLI_02', status='error')
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            data = request.data
            old_seat_number = instance.seat_number
            old_seat_type = instance.type

            # Get available_seat from the provided value
            available_seat = instance.flight.plane.seats.filter(
                type=data['type'],
                seat_number=data['seat_number'],
                reserved=False,
                deleted=False,
                booked=False).first()

            if available_seat is not None:

                # Change status of the seat to reserved and assign the new seat.
                available_seat.reserved = True
                instance.type = available_seat.type
                instance.seat_number = available_seat.seat_number

                available_seat.save()
                instance.save()

                # Free up the old seat.
                old_seat = instance.flight.plane.seats.filter(
                    type=old_seat_type,
                    seat_number=old_seat_number,
                    deleted=False).first()
                old_seat.reserved = False
                old_seat.save()

                res = ResponseHandler.response(
                    data=MESSAGES['RESERVED'].format(
                        available_seat.seat_number,
                        instance.flight.flight_number))
                return Response(res)

            error = ResponseHandler.response({}, key='FLI_01', status='error')
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        error = ResponseHandler.response(serializer.errors,
                                         key='USR_O3',
                                         status='error')
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        """
        Default get objects.
        """
        query_set = self.get_queryset()
        obj = generics.get_object_or_404(query_set, **self.kwargs)
        return obj

    def get_queryset(self):
        """
        default query set.
        """

        return Reservation.objects.filter(made_by=self.request.user,
                                          deleted=False,
                                          booked=False)


class TicketView(generics.CreateAPIView, generics.ListAPIView):
    """
    View set for Tickets.
    """

    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """Method to list tickets booked."""

        pass

    def create(self, request, *args, **kwargs):
        """
        Method to create a ticket."""
        pass

    def get_queryset(self):
        """
        Default query set.
        """

        return Ticket.objects.filter(
            made_by=self.request.user,
            deleted=False,
        )
