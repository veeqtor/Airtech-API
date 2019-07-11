"""Test module for the plane model"""

import pytest
from tests.fixtures.plane import NEW_PLANE, SEATS

pytestmark = pytest.mark.django_db


class TestPlaneAndSeatModel:
    """Test plane model"""

    def test_the_model_string_for_plane_succeeds(self, add_planes):
        """Test that plane model string rep is correct."""

        plane = add_planes[0]
        assert plane.__str__() == f'{plane.model}'

    def test_plane_creation_succeeds(self, add_planes):
        """
        Test that a plane model can be successfully created.
        """
        plane = add_planes[0]

        assert plane.model == NEW_PLANE[0]['model']
        assert plane.grounded == NEW_PLANE[0]['grounded']
        assert plane.seats is not None
        assert len(plane.get_seats) > 1

    def test_plane_deletion_succeeds(self, add_planes):
        """
        Test plane deletion
        """

        plane = add_planes[0]
        plane.delete()

        assert plane.deleted

    def test_plane_hard_deletion_succeeds(self, add_planes):
        """
        Test plane hard deletion
        """

        plane = add_planes[0]
        plane.hard_delete()

        assert plane.id is None

    # SEATS TESTS

    def test_the_model_string_for_seats_succeeds(self, add_seats):
        """Test that seat model string rep is correct."""

        seat = add_seats[0]
        assert seat.__str__() == f'{seat.type} - {seat.seat_number}'

    def test_seat_creation_succeeds(self, add_seats):
        """
        Test that a seat model can be successfully created.
        """
        seat = add_seats[0]

        assert seat.type == SEATS[0]['type']
        assert seat.seat_number == SEATS[0]['seat_number']

    def test_seat_deletion_succeeds(self, add_seats):
        """
        Test seat deletion
        """

        seat = add_seats[0]
        seat.delete()

        assert seat.deleted

    def test_seat_hard_deletion_succeeds(self, add_seats):
        """
        Test seat hard deletion
        """

        seat = add_seats[0]
        seat.hard_delete()

        assert seat.id is None
