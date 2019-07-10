"""User Flight Serializers"""

from rest_framework import serializers
from src.apps.flight.models import Plane, Flight, Seats


class SeatsSerializer(serializers.ModelSerializer):
    """Class representing the Seats serializer"""

    class Meta:
        """Meta class"""

        model = Seats
        fields = ('id', 'type', 'booked', 'reserved', 'seat_number')


class AvailableSeatsSerializer(SeatsSerializer):
    """Class representing the Available Seats serializer"""

    class Meta(SeatsSerializer.Meta):
        """Meta class"""

        fields = ('id', 'type', 'seat_number')


class PlaneSerializer(serializers.ModelSerializer):
    """Class representing the Plane serializer"""

    seats = SeatsSerializer(many=True)

    class Meta:
        """Meta class"""

        model = Plane
        fields = ('id', 'model', 'grounded', 'seats')

    def create(self, validated_data):
        """Custom create"""

        seats = validated_data.pop('seats')
        instance = super(self.__class__, self).create(validated_data)

        for seat in seats:
            seat_instance = Seats.objects.create(**seat)
            instance.seats.add(seat_instance)
            instance.save()

        return instance

    def update(self, instance, validated_data):
        """Custom Update"""

        seats = validated_data.pop('seats', None)
        instance = super(self.__class__, self).update(instance, validated_data)

        if seats is not None:
            [instance.seats.remove(seat) for seat in instance.seats.all()]

            for seat in seats:
                seat_instance = Seats.objects.create(**seat)
                instance.seats.add(seat_instance)
                instance.save()

            return instance

        return instance


class PlaneModelSerializer(PlaneSerializer):
    """Class representing the Plane model serializer"""

    class Meta(PlaneSerializer.Meta):
        """Meta class"""

        fields = ('id', 'model', 'grounded')


class FlightSerializer(serializers.ModelSerializer):
    """Class representing the Flight serializer"""

    class Meta:
        """Meta class"""

        model = Flight
        fields = ('id', 'plane', 'flight_number', 'price', 'take_off',
                  'destination', 'date', 'departure_time', 'arrival_time',
                  'flight_duration')
        read_only_fields = ('flight_duration', )


class FlightWithPlaneSerializer(FlightSerializer):
    """Class representing the flight serializer"""

    plane = PlaneModelSerializer()


class StatusSerializer(FlightSerializer):
    """Class for status serializer"""

    class Meta(FlightSerializer.Meta):
        """Meta"""

        fields = ('status', )
