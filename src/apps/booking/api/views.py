"""Module for the bookings views."""
from datetime import timedelta, date
from django.conf import settings

from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from src.services.user_emails import UserEmails
from src.apps.core.views import BaseModelViewSet
from src.apps.core.utilities.response_utils import ResponseHandler
from src.apps.core.utilities.messages import MESSAGES
from src.apps.booking.models import (Reservation, Ticket)
from src.apps.flight.models import Flight
from src.apps.booking.api.serializers import (ReservationSerializer,
                                              TicketSerializer)


class ReservationsViewSet(BaseModelViewSet):
    """
    View set for Reservations.
    """
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

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
                    UserEmails.reservation_email(request.user.id,
                                                 reservation_saved,
                                                 context=request)

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

        # Check if the dates are within edit range
        if (flight_date - today) <= timedelta(
                days=settings.FLIGHT_EDIT_ALLOWANCE_DAYS):  # noqa W504
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

    @action(detail=True)
    def cancel(self, request, *args, **kwargs):  # noqa: F401
        """
        Cancel a reservation.
        """
        instance = self.get_object()
        today = date.today()
        flight_date = instance.flight.date

        # Check if the dates are within edit range
        if (flight_date - today) <= timedelta(
                days=settings.FLIGHT_EDIT_ALLOWANCE_DAYS):  # noqa W504
            error = ResponseHandler.response({}, key='FLI_02', status='error')
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        # Free up the seat.
        seat = instance.flight.plane.seats.filter(
            type=instance.type,
            seat_number=instance.seat_number,
            deleted=False).first()

        seat.reserved = False
        seat.save()
        instance.delete()

        res = ResponseHandler.response(data=MESSAGES['RESERVE_CANCEL'].format(
            instance.flight.flight_number))
        return Response(res)

    def get_queryset(self):
        """
        default query set.
        """

        return Reservation.objects.filter(made_by=self.request.user,
                                          deleted=False,
                                          booked=False)


class TicketViewSet(BaseModelViewSet):
    """
    View set for Tickets.
    """

    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Method to create a ticket.
        """

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            data = request.data

            flight_qs = Flight \
                .objects.filter(pk=data['flight'],
                                plane__grounded=False,
                                plane__seats__type=data['type'],
                                plane__seats__seat_number=data['seat_number'],
                                plane__seats__reserved=False,
                                plane__seats__booked=False,
                                plane__seats__deleted=False) \
                .select_related('plane').prefetch_related('plane__seats') \
                .first()

            if flight_qs is None:
                error = ResponseHandler.response({},
                                                 key='FLI_01',
                                                 status='error')
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            available_seat = flight_qs.plane.seats.get(
                type=data['type'],
                seat_number=data['seat_number'],
                reserved=False,
                booked=False,
                deleted=False)

            ticket = {
                'ticket_ref': f'{flight_qs.flight_number}{available_seat.type}'
                f'-{available_seat.seat_number}',
                'flight': flight_qs,
                'type': available_seat.type,
                'seat_number': available_seat.seat_number,
                'made_by': request.user
            }

            ticket_saved = Ticket.objects.create(**ticket)

            if ticket_saved:
                available_seat.reserved = True
                available_seat.booked = True
                available_seat.save()

                res = ResponseHandler.response(data=MESSAGES['BOOKED'].format(
                    available_seat.seat_number, flight_qs.flight_number))

                return Response(res)

        error = ResponseHandler.response(serializer.errors,
                                         key='USR_O3',
                                         status='error')
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """Method to edit a ticket."""

        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=True)
        today = date.today()
        flight_date = instance.flight.date

        # Check if the dates are within edit range
        if (flight_date - today) <= timedelta(
                days=settings.FLIGHT_EDIT_ALLOWANCE_DAYS):  # noqa W504
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

            if available_seat is None:
                error = ResponseHandler.response({},
                                                 key='FLI_01',
                                                 status='error')
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            # Change status of the seat to reserved and assign the new seat.
            available_seat.reserved = True
            available_seat.booked = True
            instance.type = available_seat.type
            instance.seat_number = available_seat.seat_number

            available_seat.save()
            instance.save()

            # Free up the old seat.
            old_seat = instance.flight.plane.seats.filter(
                type=old_seat_type, seat_number=old_seat_number,
                deleted=False).first()
            old_seat.reserved = False
            old_seat.booked = False
            old_seat.save()

            res = ResponseHandler.response(data=MESSAGES['BOOKED'].format(
                available_seat.seat_number, instance.flight.flight_number))
            return Response(res)

        error = ResponseHandler.response(serializer.errors,
                                         key='USR_O3',
                                         status='error')
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def cancel(self, request, *args, **kwargs):  # noqa: F401
        """
        Cancel a booking.
        """

        instance = self.get_object()
        today = date.today()
        flight_date = instance.flight.date

        # Check if the dates are within edit range
        if (flight_date - today) <= timedelta(
                days=settings.FLIGHT_EDIT_ALLOWANCE_DAYS):  # noqa W504
            error = ResponseHandler.response({}, key='FLI_02', status='error')
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        # Free up the seat.
        seat = instance.flight.plane.seats.filter(
            type=instance.type,
            seat_number=instance.seat_number,
            deleted=False).first()

        seat.reserved = False
        seat.booked = False
        seat.save()
        instance.delete()

        res = ResponseHandler.response(data=MESSAGES['TICKET_CANCEL'].format(
            instance.flight.flight_number))
        return Response(res)

    def get_queryset(self):
        """
        Default query set.
        """

        return Ticket.objects.filter(
            made_by=self.request.user,
            deleted=False,
        )
