"""Test module for the flight endpoint"""

import pytest
from django.urls import resolve, reverse

from src.apps.core.utilities.messages import ERRORS
from tests.fixtures.flight import NEW_FLIGHT
from tests.fixtures.user import USER

FLIGHT_GET_URL = reverse('flight:flight-list')
GET_A_FLIGHT_URL = 'flight:flight-detail'


@pytest.mark.django_db
class TestFlightView:
    """Class to test the flight views"""

    def test_flight_get_url_succeeds(self):
        """Test the paths"""

        assert resolve(FLIGHT_GET_URL).view_name == 'flight:flight-list'
        assert resolve(reverse('flight:flight-detail',
                               args=['pk'
                                     ])).view_name == 'flight:flight-detail'

    def test_getting_all_flights_succeeds(self, add_flights, auth_header,
                                          client):
        """Test getting available flights."""

        response = client.get(FLIGHT_GET_URL, **auth_header)
        resp_data = response.data
        data = resp_data['data']
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert len(data) == 2
        assert data[0]['price'] == str(NEW_FLIGHT['price'])

    def test_getting_all_flights_without_auth_fails(self, client):
        """Test getting available flights fails"""

        response = client.get(FLIGHT_GET_URL)
        resp_data = response.data
        assert response.status_code == 401
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['AUTH_01']

    def test_getting_a_flight_succeeds(self, client, auth_header, add_flights):
        """Test getting a flights"""

        flight = add_flights[0]
        flight_url = reverse(GET_A_FLIGHT_URL, args=[flight.id])

        response = client.get(flight_url, **auth_header)
        resp_data = response.data
        data = resp_data['data']
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert isinstance(data['plane'], dict)
        assert data['flight_number'] is not None

    def test_getting_available_seats_in_a_flight_succeeds(
            self, client, auth_header, add_flights):
        """Test getting a flights"""

        flight = add_flights[0]
        available_seats_url = 'flight:flight-available-seats'
        flight_url = reverse(available_seats_url, args=[flight.id])
        response = client.get(flight_url, {'type': 'BUS'}, **auth_header)
        client.get(flight_url, {'type': 'ECO'}, **auth_header)
        client.get(flight_url, **auth_header)
        resp_data = response.data
        data = resp_data['data']
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert isinstance(data, list)
        assert data[0]['seat_number'] is not None

    def test_getting_a_flights_without_auth_fails(self, client, add_flights):
        """Test getting a flights fails"""

        flight = add_flights[0]
        flight_url = reverse(GET_A_FLIGHT_URL, args=[flight.id])

        response = client.get(flight_url)
        resp_data = response.data
        assert response.status_code == 401
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['AUTH_01']

    def test_getting_a_flights_with_invalid_pk_fails(self, client,
                                                     auth_header):
        """Test getting a flights fails"""

        flight_url = reverse(GET_A_FLIGHT_URL, args=['invalid'])

        response = client.get(flight_url, **auth_header)
        resp_data = response.data
        assert response.status_code == 404
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['USR_09']

    def test_users_creating_a_flight_fails(self, client, add_planes,
                                           auth_header):
        """Test that admin should be able to create flights"""

        plane = add_planes[0].id

        NEW_FLIGHT['plane'] = plane
        NEW_FLIGHT['flight_number'] = 'Fl-123TS'

        response = client.post(FLIGHT_GET_URL,
                               content_type='application/json',
                               data=NEW_FLIGHT,
                               **auth_header)

        resp_data = response.data
        assert response.status_code == 403
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['AUTH_02']

    def test_only_admin_can_create_flights_succeed(self, client, add_planes,
                                                   create_superuser,
                                                   generate_token):
        """Test that admin should be able to create flights"""
        user = create_superuser(USER)
        token = generate_token(user)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        plane_id = add_planes[0].id

        NEW_FLIGHT['plane'] = plane_id
        NEW_FLIGHT['flight_number'] = 'Fl-123TS'

        response = client.post(FLIGHT_GET_URL,
                               content_type='application/json',
                               data=NEW_FLIGHT,
                               **auth_header)
        resp_data = response.data
        data = resp_data['data']
        assert response.status_code == 201
        assert resp_data['status'] == 'success'
        assert data['flight_number'] == NEW_FLIGHT['flight_number']
        assert data['plane'] == plane_id

    def test_creating_a_flight_with_invalid_data_fails(self, client,
                                                       create_superuser,
                                                       generate_token):
        """Test create flight with invalid data"""

        user = create_superuser(USER)
        token = generate_token(user)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        NEW_FLIGHT['flight_number'] = ''

        response = client.post(FLIGHT_GET_URL,
                               content_type='application/json',
                               data=NEW_FLIGHT,
                               **auth_header)
        resp_data = response.data
        data = resp_data['errors']

        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert data['flight_number'][0] == ERRORS['USR_07']

    def test_admin_can_update_flights_with_invalid_id_fails(
            self, client, add_planes, create_superuser, generate_token):
        """Test that admin should not be able to update a flights with
        invalid param id"""

        user = create_superuser(USER)
        token = generate_token(user)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        plane_id = add_planes[0].id
        flight_url = reverse(GET_A_FLIGHT_URL, args=['invalid'])

        NEW_FLIGHT['plane'] = plane_id
        NEW_FLIGHT['flight_number'] = 'Fl-123TS'

        response = client.patch(flight_url,
                                content_type='application/json',
                                data=NEW_FLIGHT,
                                **auth_header)
        resp_data = response.data
        assert response.status_code == 404
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['USR_09']

    def test_updating_a_flight_with_invalid_data_fails(self, add_flights,
                                                       client,
                                                       create_superuser,
                                                       generate_token):
        """Test update flight with invalid data"""
        user = create_superuser(USER)
        token = generate_token(user)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        flight = add_flights[0]
        flight_url = reverse(GET_A_FLIGHT_URL, args=[flight.id])

        NEW_FLIGHT['flight_number'] = ''

        response = client.patch(flight_url,
                                content_type='application/json',
                                data=NEW_FLIGHT,
                                **auth_header)
        resp_data = response.data
        data = resp_data['errors']

        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert data['flight_number'][0] == ERRORS['USR_07']

    def test_only_admin_can_update_a_flight_succeeds(self, client,
                                                     create_superuser,
                                                     generate_token,
                                                     add_planes, add_flights):
        """Test that admin should be able to update flight"""

        user = create_superuser(USER)
        token = generate_token(user)
        plane_id = add_planes[1].id
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        flight = add_flights[0]
        flight_url = reverse(GET_A_FLIGHT_URL, args=[flight.id])

        NEW_FLIGHT['plane'] = plane_id
        NEW_FLIGHT['flight_number'] = 'EUT-123IR'

        response = client.patch(flight_url,
                                content_type='application/json',
                                data=NEW_FLIGHT,
                                **auth_header)
        resp_data = response.data
        data = resp_data['data']

        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert data['flight_number'] == NEW_FLIGHT['flight_number']
        assert data['plane'] == plane_id

    def test_users_cannot_update_a_flight_fails(self, client, auth_header,
                                                add_planes, add_flights):
        """Test that admin should be able to update flight"""
        plane_id = add_planes[1].id
        flight = add_flights[0]
        flight_url = reverse(GET_A_FLIGHT_URL, args=[flight.id])

        NEW_FLIGHT['plane'] = plane_id
        NEW_FLIGHT['flight_number'] = 'EUT-123IR'

        response = client.patch(flight_url,
                                content_type='application/json',
                                data=NEW_FLIGHT,
                                **auth_header)
        resp_data = response.data
        assert response.status_code == 403
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['AUTH_02']
