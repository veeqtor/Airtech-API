"""Module to test user registration"""

import pytest
from django.urls import resolve, reverse
from tests.fixtures.user import USER
from src.apps.core.utilities.messages import ERRORS

REGISTER_URL = reverse('user:register')


@pytest.mark.django_db
class TestUserRegistration:
    """Class to test out the user registration"""

    def test_user_url_succeeds(self):
        """Test the paths"""
        assert resolve(REGISTER_URL).view_name == 'user:register'

    def test_user_account_registration_succeeds(self, client):
        """Test that users can register"""

        response = client.post(REGISTER_URL, data={**USER})
        resp_data = response.data

        assert response.status_code == 201
        assert resp_data['status'] == 'success'
        assert resp_data['data']['token'] is not None

    def test_user_duplicate_account_registration_false(self, client,
                                                       create_user):
        """Test that users cannot have a duplicate account."""

        create_user(USER)
        response = client.post(REGISTER_URL, data={**USER})
        resp_data = response.data
        errors = resp_data['errors']

        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['USR_O3']
        assert errors['email'][0] == ERRORS['USR_05']

    def test_user_account_registration_with_no_data_fails(self, client):
        """Test that users cannot register without data"""

        response = client.post(REGISTER_URL, data={})
        resp_data = response.data
        errors = resp_data['errors']
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['USR_O3']
        assert errors['email'][0] == ERRORS['USR_04']
        assert errors['password'][0] == ERRORS['USR_04']

    def test_user_account_registration_with_invalid_data_fails(self, client):
        """Test that users cannot register without invalid data"""

        response = client.post(REGISTER_URL,
                               data={
                                   'email': 'user_example.com',
                                   'password': 'Password1234'
                               })
        resp_data = response.data
        errors = resp_data['errors']
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['USR_O3']
        assert errors['email'][0] == ERRORS['USR_01']
        assert errors['password'][0] == ERRORS['USR_02']
