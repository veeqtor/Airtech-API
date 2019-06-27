"""Test module for the flight model"""

import pytest
from tests.fixtures.flight import NEW_FLIGHT, DURATION

pytestmark = pytest.mark.django_db


class TestFlightModel:
    """Test flight model"""

    def test_the_model_string_succeeds(self, add_flights):
        """Test that flight model string rep is correct."""

        flight = add_flights[0]
        assert flight.__str__(
        ) == f'{flight.flight_number} - ' \
            f'{flight.take_off} to {flight.destination}'

    def test_flight_creation_succeeds(self, add_flights):
        """
        Test that a flight model can be successfully created.
        """
        flight = add_flights[0]

        # assert flight.flight_number == NEW_FLIGHT['flight_number']
        assert flight.price == NEW_FLIGHT['price']
        assert flight.take_off == NEW_FLIGHT['take_off']
        assert flight.destination == NEW_FLIGHT['destination']
        assert flight.date is not None
        assert flight.departure_time == NEW_FLIGHT['departure_time']
        assert flight.arrival_time == NEW_FLIGHT['arrival_time']
        assert flight.flight_duration == str(DURATION)
        assert flight.plane is not None

    def test_flight_deletion_succeeds(self, add_flights):
        """
        Test flight deletion
        """

        flight = add_flights[0]
        flight.delete()

        assert flight.deleted

    def test_flight_hard_deletion_succeeds(self, add_flights):
        """
        Test flight hard deletion
        """

        flight = add_flights[0]
        flight.hard_delete()

        assert flight.id is None
