"""Test module for the reservation endpoint"""

import pytest
from django.urls import resolve, reverse

from src.apps.core.utilities.messages import ERRORS, MESSAGES

RESERVATION_URL = reverse('booking:reservation')


@pytest.mark.django_db
class TestReservationView:
    """Class to test the reservation views"""

    def test_reservation_url_succeeds(self):
        """Test the paths"""

        assert resolve(RESERVATION_URL).view_name == 'booking:reservation'

    def test_making_a_reservation_succeeds(self, auth_header, client,
                                           add_flights):
        """Test making a reservation"""

        flight = add_flights[0]
        seats = flight.plane.seats.all()

        data = {
            'flight': flight.id,
            'type': seats[0].type,
            'seat_number': seats[0].seat_number
        }

        response = client.post(RESERVATION_URL,
                               data=data,
                               content_type='application/json',
                               **auth_header)
        resp_data = response.data
        data = resp_data['data']
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert data == MESSAGES['RESERVED'].format(seats[0].seat_number,
                                                   flight.flight_number)

    def test_user_cannot_make_a_reservation_with_invalid_data_fails(
            self, auth_header, client, add_flights):
        """Test making a reservation"""

        flight = add_flights[0]
        seats = flight.plane.seats.all()

        data = {
            'flight': flight.id,
            'type': seats[0].type,
            'seat_number': 'invalid'
        }

        response = client.post(RESERVATION_URL,
                               data=data,
                               content_type='application/json',
                               **auth_header)
        resp_data = response.data
        message = resp_data['user_message']

        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert message == ERRORS['FLI_01']

    def test_user_cannot_make_a_reservation_on_already_booked_seats_fails(
            self, auth_header, client, add_flights):
        """Test making a reservation"""

        flight = add_flights[0]
        seats = flight.plane.seats.first()
        seats.reserved = True
        seats.booked = True
        seats.save()

        data = {
            'flight': flight.id,
            'type': seats.type,
            'seat_number': seats.seat_number
        }

        response = client.post(RESERVATION_URL,
                               data=data,
                               content_type='application/json',
                               **auth_header)
        resp_data = response.data
        message = resp_data['user_message']
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert message == ERRORS['FLI_01']

    def test_user_cannot_make_a_reservation_with_empty_data_fails(
            self, auth_header, client, add_flights):
        """Test making a reservation"""

        flight = add_flights[0]
        seats = flight.plane.seats.all()
        seats[0].reserved = True
        seats[0].booked = True
        seats[0].save()

        data = {'flight': '', 'type': 'ECO', 'seat_number': ''}

        response = client.post(RESERVATION_URL,
                               data=data,
                               content_type='application/json',
                               **auth_header)
        resp_data = response.data
        errors = resp_data['errors']
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert errors['seat_number'][0] == ERRORS['USR_07']
