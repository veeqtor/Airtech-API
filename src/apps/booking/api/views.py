"""Module for the bookings views."""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from src.apps.core.utilities.response_utils import ResponseHandler
from src.apps.core.utilities.messages import ERRORS, MESSAGES
from src.apps.booking.models import (Reservation, Ticket)
from src.apps.flight.models import Flight, Seats
from src.apps.booking.api.serializers import (ReservationSerializer,
                                              TicketSerializer)


class ReservationsView(generics.CreateAPIView, generics.ListAPIView,
                       generics.RetrieveAPIView):
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
