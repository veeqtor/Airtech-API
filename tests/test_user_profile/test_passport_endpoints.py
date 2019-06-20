"""Test module for the passport endpoint"""

import pytest
from django.urls import resolve, reverse

from src.apps.core.utilities.messages import ERRORS
from tests.fixtures.passport import (NEW_PASSPORT, EDIT_PASSPORT,
                                     INVALID_PASSPORT)

PASSPORT_URL = reverse('user:passports-list')


@pytest.mark.django_db
class TestUserPassportView:
    """Class to test the passport views"""

    def test_profile_url_succeeds(self):
        """Test the paths"""

        assert resolve(PASSPORT_URL).view_name == 'user:passports-list'

    def test_getting_a_logged_in_passport_with_no_passport_succeeds(
            self, auth_header, client):
        """Test getting a logged in user without passport"""

        response = client.get(PASSPORT_URL, **auth_header)
        resp_data = response.data

        data = resp_data['data']
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert len(data) == 0
        assert isinstance(data, list)

    def test_adding_a_new_passport_succeeds(self, auth_header, client):
        """Test getting a logged in user without passport"""

        response = client.post(PASSPORT_URL,
                               data=NEW_PASSPORT,
                               content_type='application/json',
                               **auth_header)

        resp_data = response.data
        data = resp_data['data']
        assert response.status_code == 201
        assert resp_data['status'] == 'success'
        assert data['image'] == NEW_PASSPORT['image']
        assert data['passport_number'] == NEW_PASSPORT['passport_number']
        assert data['issued_date'] == NEW_PASSPORT['issued_date']
        assert data['expiry_date'] == NEW_PASSPORT['expiry_date']

    def test_duplicate_passports_fails(self, add_passports, generate_token,
                                       client):
        """Test that a user cannot add an already existing passport"""

        passports = add_passports
        user = passports[0].profile.user
        token = generate_token(user)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        response = client.post(PASSPORT_URL,
                               data=NEW_PASSPORT,
                               content_type='application/json',
                               **auth_header)

        resp_data = response.data

        errors = resp_data['errors']
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert errors['passport_number'][0] == ERRORS['CUST_01'].format(
            'passport', 'Passport Number')

    def test_getting_a_logged_in_users_passports_succeeds(
            self, client, generate_token, add_passports):
        """Test getting a logged in user passport"""

        passports = add_passports
        user = passports[0].profile.user
        token = generate_token(user)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        response = client.get(PASSPORT_URL, **auth_header)
        resp_data = response.data
        data = resp_data['data']

        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert len(data) >= 1
        assert data[0]['passport_number'] == passports[-1].passport_number
        assert data[-1]['passport_number'] == passports[0].passport_number

    def test_get_a_logged_in_users_passport_succeeds(self, client,
                                                     generate_token,
                                                     add_passports):
        """Test getting a logged in user passport"""

        passports = add_passports
        passport_url = reverse('user:passports-detail', args=[passports[0].id])
        user = passports[0].profile.user
        token = generate_token(user)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        response = client.get(passport_url, **auth_header)
        resp_data = response.data
        data = resp_data['data']

        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert data['passport_number'] == passports[0].passport_number
        assert data['passport_number'] == passports[0].passport_number

    def test_get_a_logged_in_users_passport_with_invalid_id_fails(
            self, client, generate_token, add_passports):
        """Test getting a logged in user passport"""

        passports = add_passports
        passport_url = reverse('user:passports-detail', args=['invalid'])
        user = passports[0].profile.user
        token = generate_token(user)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        response = client.get(passport_url, **auth_header)
        resp_data = response.data
        assert response.status_code == 404
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['USR_09']

    def test_that_user_can_modify_passports_succeeds(self, client,
                                                     generate_token,
                                                     add_passports):
        passports = add_passports
        passport_url = reverse('user:passports-detail', args=[passports[0].id])
        user = passports[0].profile.user
        token = generate_token(user)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        response = client.patch(passport_url,
                                data=EDIT_PASSPORT,
                                content_type='application/json',
                                **auth_header)

        resp_data = response.data
        data = resp_data['data']
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert data['issued_date'] == EDIT_PASSPORT['issued_date']
        assert data['expiry_date'] == EDIT_PASSPORT['expiry_date']

    def test_that_user_cannot_modify_passports_with_empty_fields_fails(
            self, client, generate_token, add_passports):
        passports = add_passports
        passport_url = reverse('user:passports-detail', args=[passports[0].id])
        user = passports[0].profile.user
        token = generate_token(user)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        response = client.patch(passport_url,
                                data=INVALID_PASSPORT,
                                content_type='application/json',
                                **auth_header)

        resp_data = response.data
        errors = resp_data['errors']
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert errors['country'][0] == ERRORS['USR_07']

    def test_that_user_can_delete_a_passport_fails(self, client,
                                                   generate_token,
                                                   add_passports):
        passports = add_passports
        passport_url = reverse('user:passports-detail', args=[passports[0].id])
        user = passports[0].profile.user
        token = generate_token(user)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        response = client.delete(passport_url, **auth_header)
        assert response.status_code == 204
