"""Test module for the tickets endpoint"""

import pytest
from datetime import date, timedelta
from django.urls import resolve, reverse
from django.conf import settings

from src.apps.core.utilities.messages import ERRORS, MESSAGES

TICKET_URL = reverse('booking:ticket-list')
TICKET_URL_DETAIL = 'booking:ticket-detail'
TICKET_URL_CANCEL = 'booking:ticket-cancel'


@pytest.mark.django_db
class TestTicketView:
    """Class to test the ticket views"""

    def test_reservation_url_succeeds(self):
        """Test the paths"""

        assert resolve(TICKET_URL).view_name == 'booking:ticket-list'

    def test_making_a_ticket_succeeds(self, auth_header, client, add_flights):
        """Test making a ticket"""

        flight = add_flights[0]
        seats = flight.plane.seats.all()

        data = {
            'flight': flight.id,
            'type': seats[0].type,
            'seat_number': seats[0].seat_number
        }

        response = client.post(TICKET_URL,
                               data=data,
                               content_type='application/json',
                               **auth_header)
        resp_data = response.data
        data = resp_data['data']
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert data == MESSAGES['BOOKED'].format(seats[0].seat_number,
                                                 flight.flight_number)

    def test_user_cannot_make_a_ticket_with_invalid_data_fails(
            self, auth_header, client, add_flights):
        """Test making a ticket"""

        flight = add_flights[0]
        seats = flight.plane.seats.all()

        data = {
            'flight': flight.id,
            'type': seats[0].type,
            'seat_number': 'invalid'
        }

        response = client.post(TICKET_URL,
                               data=data,
                               content_type='application/json',
                               **auth_header)
        resp_data = response.data
        message = resp_data['user_message']

        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert message == ERRORS['FLI_01']

    def test_user_cannot_make_a_ticket_on_already_booked_seats_fails(
            self, auth_header, client, add_flights):
        """Test making a ticket fails."""

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

        response = client.post(TICKET_URL,
                               data=data,
                               content_type='application/json',
                               **auth_header)
        resp_data = response.data
        message = resp_data['user_message']
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert message == ERRORS['FLI_01']

    def test_user_cannot_make_a_ticket_with_empty_data_fails(
            self, auth_header, client, add_flights):
        """Test making a ticket fails"""

        flight = add_flights[0]
        seats = flight.plane.seats.all()
        seats[0].reserved = True
        seats[0].booked = True
        seats[0].save()

        data = {'flight': '', 'type': 'ECO', 'seat_number': ''}

        response = client.post(TICKET_URL,
                               data=data,
                               content_type='application/json',
                               **auth_header)
        resp_data = response.data
        errors = resp_data['errors']
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert errors['seat_number'][0] == ERRORS['USR_07']

    def test_getting_all_ticket_succeeds(self, generate_token, add_tickets,
                                         client):
        """Test getting ticket made by a logged in user"""

        ticket = add_tickets[0]
        token = generate_token(ticket.made_by)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        response = client.get(TICKET_URL, **auth_header)
        resp_data = response.data

        data = resp_data['data']
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert len(data) == 2
        assert isinstance(data, list)

    def test_user_cancel_allowance_days_for_reservation_for_a_period_of_time(
            self, add_tickets, generate_token, client):
        """Test that users cannot cancel the ticket before a period of
        time."""

        ticket = add_tickets[0]
        flight = ticket.flight
        flight.date = date.today() + timedelta(days=4)
        flight.save()
        token = generate_token(ticket.made_by)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        ticket_url = reverse(TICKET_URL_CANCEL, args=[ticket.id])

        response = client.get(ticket_url, **auth_header)
        resp_data = response.data
        message = resp_data['user_message']
        assert response.status_code == 403
        assert resp_data['status'] == 'error'
        assert message == ERRORS['FLI_02']

    def test_user_cancel_tickets(self, add_tickets, generate_token, client):
        """Test that users cannot cancel the tickets before a period of
        time."""

        ticket = add_tickets[0]
        flight = ticket.flight
        token = generate_token(ticket.made_by)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        ticket_url = reverse(TICKET_URL_CANCEL, args=[ticket.id])

        response = client.get(ticket_url, **auth_header)
        resp_data = response.data
        data = resp_data['data']

        seat = flight.plane.seats.get(type=ticket.type,
                                      seat_number=ticket.seat_number)
        assert seat.reserved is False
        assert seat.booked is False
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert data == MESSAGES['TICKET_CANCEL'].format(flight.flight_number)

    def test_user_can_edit_ticket_succeeds(self, add_tickets, generate_token,
                                           client):
        """
        Test that users can edit there tickets.
        """

        ticket = add_tickets[0]
        token = generate_token(ticket.made_by)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        flight = ticket.flight
        seats = flight.plane.seats.first()
        ticket_url = reverse(TICKET_URL_DETAIL, args=[ticket.id])

        data = {'type': seats.type, 'seat_number': seats.seat_number}

        response = client.patch(ticket_url,
                                content_type='application/json',
                                data=data,
                                **auth_header)
        resp_data = response.data
        data = resp_data['data']
        seat = flight.plane.seats.get(type=ticket.type,
                                      seat_number=ticket.seat_number)

        assert seat.reserved is False
        assert seat.booked is False
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert data == MESSAGES['BOOKED'].format(seats.seat_number,
                                                 flight.flight_number)

    def test_user_can_edit_tickets_fails(self, add_tickets, generate_token,
                                         client):
        """
        Test that users can edit there ticket fails.
        """

        ticket = add_tickets[0]
        token = generate_token(ticket.made_by)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        flight = ticket.flight
        seats = flight.plane.seats.first()
        ticket_url = reverse(TICKET_URL_DETAIL, args=[ticket.id])

        data = {'type': seats.type, 'seat_number': ''}

        response = client.patch(ticket_url,
                                content_type='application/json',
                                data=data,
                                **auth_header)
        resp_data = response.data
        errors = resp_data['errors']
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert errors['seat_number'][0] == ERRORS['USR_07']

    def test_user_can_edit_same_ticket_fails(self, add_tickets, generate_token,
                                             client):
        """
        Test that users can edit there ticket fails.
        """
        ticket = add_tickets[0]
        flight = ticket.flight
        seat = flight.plane.seats.get(type=ticket.type,
                                      seat_number=ticket.seat_number)
        seat.reserved = True
        seat.booked = True
        seat.save()
        token = generate_token(ticket.made_by)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        ticket_url = reverse(TICKET_URL_DETAIL, args=[ticket.id])
        data = {'type': ticket.type, 'seat_number': ticket.seat_number}
        response = client.patch(ticket_url,
                                content_type='application/json',
                                data=data,
                                **auth_header)
        resp_data = response.data
        message = resp_data['user_message']
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert message == ERRORS['FLI_01']

    def test_user_edit_allowance_days_for_ticket_for_a_period_of_time(
            self, add_tickets, generate_token, client):
        """
        Test that users cannot edit the tickets after a period of time.
        """

        ticket = add_tickets[0]
        flight = ticket.flight
        flight.date = date.today() + timedelta(days=4)
        flight.save()
        token = generate_token(ticket.made_by)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        ticket_url = reverse(TICKET_URL_DETAIL, args=[ticket.id])

        data = {'type': ticket.type, 'seat_number': ticket.seat_number}
        response = client.patch(ticket_url,
                                content_type='application/json',
                                data=data,
                                **auth_header)
        resp_data = response.data
        message = resp_data['user_message']
        assert response.status_code == 403
        assert resp_data['status'] == 'error'
        assert message == ERRORS['FLI_02']
