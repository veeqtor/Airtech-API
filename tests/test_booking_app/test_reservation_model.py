"""Test module for the reservation model"""

import pytest

pytestmark = pytest.mark.django_db


class TestReservationModel:
    """Test reservation model"""

    def test_the_model_string_succeeds(self, add_reservations):
        """Test that reservation model string rep is correct."""

        reservation = add_reservations[0]
        assert reservation.__str__(
        ) == f'{reservation.flight} - {reservation.seat_number}'

    def test_reservation_creation_succeeds(self, add_reservations):
        """
        Test that a reservation model can be successfully created.
        """
        reservation = add_reservations[0]

        assert reservation.flight is not None
        assert reservation.seat_number is not None
        assert reservation.booked is False
        assert reservation.type is not None
        assert reservation.made_by is not None
        assert reservation.date_made is not None

    def test_reservation_deletion_succeeds(self, add_reservations):
        """
        Test reservation deletion
        """

        reservation = add_reservations[0]
        reservation.delete()

        assert reservation.deleted

    def test_reservation_hard_deletion_succeeds(self, add_reservations):
        """
        Test reservation hard deletion
        """

        reservation = add_reservations[0]
        reservation.hard_delete()

        assert reservation.id is None
