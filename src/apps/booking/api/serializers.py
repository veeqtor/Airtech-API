"""Module for the bookings serializers."""

from rest_framework import serializers
from src.apps.booking.models import Reservation, Ticket
from src.apps.user.api.serializers import UserSerializer
from src.apps.flight.api.serializers import FlightWithPlaneSerializer


class ReservationSerializer(serializers.ModelSerializer):
    """Class representing the Reservation serializer"""

    made_by = UserSerializer(read_only=True)
    flight = FlightWithPlaneSerializer(read_only=True)

    class Meta:
        """Meta class"""

        model = Reservation
        fields = ('id', 'flight', 'seat_number', 'type', 'booked', 'made_by')
        read_only_fields = ['flight', 'booked']


class TicketSerializer(serializers.ModelSerializer):
    """Class representing the Reservation serializer"""

    class Meta:
        """Meta class"""

        model = Ticket
