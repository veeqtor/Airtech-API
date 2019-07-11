"""Test module for the reservation endpoint"""

import pytest
from datetime import date, timedelta
from django.urls import resolve, reverse
from django.core import mail

from src.apps.core.utilities.messages import ERRORS, MESSAGES

RESERVATION_URL = reverse('booking:reservation-list')
RESERVATION_URL_DETAIL = 'booking:reservation-detail'
RESERVATION_URL_CANCEL = 'booking:reservation-cancel'


@pytest.mark.django_db
class TestReservationView:
    """Class to test the reservation views"""

    def test_reservation_url_succeeds(self):
        """Test the paths"""

        assert resolve(RESERVATION_URL).view_name == 'booking:reservation-list'

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
        email = mail.outbox[1]
        data = resp_data['data']
        assert response.status_code == 200
        assert email.subject == 'Reservation'
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
        """Test making a reservation fails"""

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

    def test_getting_all_reservations_succeeds(self, generate_token,
                                               add_reservations, client):
        """Test getting reservations made by a logged in user"""
        reservation = add_reservations[0]
        token = generate_token(reservation.made_by)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        response = client.get(RESERVATION_URL, **auth_header)
        resp_data = response.data

        data = resp_data['data']
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert len(data) == 2
        assert isinstance(data, list)

    def test_user_can_edit_reservations_succeeds(self, add_reservations,
                                                 generate_token, client):
        """
        Test that users can edit there reservations.
        """
        reservation = add_reservations[0]
        token = generate_token(reservation.made_by)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        flight = reservation.flight
        seats = flight.plane.seats.first()
        reservation_url = reverse(RESERVATION_URL_DETAIL,
                                  args=[reservation.id])

        data = {'type': seats.type, 'seat_number': seats.seat_number}

        response = client.patch(reservation_url,
                                content_type='application/json',
                                data=data,
                                **auth_header)
        resp_data = response.data
        data = resp_data['data']
        seat = flight.plane.seats.get(type=reservation.type,
                                      seat_number=reservation.seat_number)

        assert seat.reserved is False
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert data == MESSAGES['RESERVED'].format(seats.seat_number,
                                                   flight.flight_number)

    def test_user_can_edit_reservations_fails(self, add_reservations,
                                              generate_token, client):
        """
        Test that users can edit there reservations fails.
        """
        reservation = add_reservations[0]
        token = generate_token(reservation.made_by)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        flight = reservation.flight
        seats = flight.plane.seats.first()
        reservation_url = reverse(RESERVATION_URL_DETAIL,
                                  args=[reservation.id])

        data = {'type': seats.type, 'seat_number': ''}

        response = client.patch(reservation_url,
                                content_type='application/json',
                                data=data,
                                **auth_header)
        resp_data = response.data
        errors = resp_data['errors']
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert errors['seat_number'][0] == ERRORS['USR_07']

    def test_user_can_edit_same_reservations_fails(self, add_reservations,
                                                   generate_token, client):
        """
        Test that users can edit there reservations fails.
        """
        reservation = add_reservations[0]
        flight = reservation.flight
        seat = flight.plane.seats.get(type=reservation.type,
                                      seat_number=reservation.seat_number)
        seat.reserved = True
        seat.save()
        token = generate_token(reservation.made_by)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        reservation_url = reverse(RESERVATION_URL_DETAIL,
                                  args=[reservation.id])
        data = {
            'type': reservation.type,
            'seat_number': reservation.seat_number
        }
        response = client.patch(reservation_url,
                                content_type='application/json',
                                data=data,
                                **auth_header)
        resp_data = response.data
        message = resp_data['user_message']
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert message == ERRORS['FLI_01']

    def test_user_edit_allowance_days_for_reservation_for_a_period_of_time(
            self, add_reservations, generate_token, client):
        """Test that users cannot edit the reservations after a period of
        time."""

        reservation = add_reservations[0]
        flight = reservation.flight
        flight.date = date.today() + timedelta(days=4)
        flight.save()
        token = generate_token(reservation.made_by)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        reservation_url = reverse(RESERVATION_URL_DETAIL,
                                  args=[reservation.id])

        data = {
            'type': reservation.type,
            'seat_number': reservation.seat_number
        }
        response = client.patch(reservation_url,
                                content_type='application/json',
                                data=data,
                                **auth_header)
        resp_data = response.data
        message = resp_data['user_message']
        assert response.status_code == 403
        assert resp_data['status'] == 'error'
        assert message == ERRORS['FLI_02']

    def test_user_cancel_allowance_days_for_reservation_for_a_period_of_time(
            self, add_reservations, generate_token, client):
        """Test that users cannot cancel the reservations before a period of
        time."""

        reservation = add_reservations[0]
        flight = reservation.flight
        flight.date = date.today() + timedelta(days=4)
        flight.save()
        token = generate_token(reservation.made_by)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        reservation_url = reverse(RESERVATION_URL_CANCEL,
                                  args=[reservation.id])

        response = client.get(reservation_url, **auth_header)
        resp_data = response.data
        message = resp_data['user_message']
        assert response.status_code == 403
        assert resp_data['status'] == 'error'
        assert message == ERRORS['FLI_02']

    def test_user_cancel_reservation(self, add_reservations, generate_token,
                                     client):
        """Test that users cannot cancel the reservations before a period of
        time."""

        reservation = add_reservations[0]
        flight = reservation.flight
        token = generate_token(reservation.made_by)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        reservation_url = reverse(RESERVATION_URL_CANCEL,
                                  args=[reservation.id])

        response = client.get(reservation_url, **auth_header)
        resp_data = response.data
        data = resp_data['data']

        seat = flight.plane.seats.get(type=reservation.type,
                                      seat_number=reservation.seat_number)
        assert seat.reserved is False
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert data == MESSAGES['RESERVE_CANCEL'].format(flight.flight_number)
