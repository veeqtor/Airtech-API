"""Module to test user login"""

import pytest
from django.urls import resolve, reverse
from tests.fixtures.user import USER, UNREGISTERED_USER, USER_INVALID
from src.apps.core.utilities.messages import ERRORS, MESSAGES

LOGIN_URL = reverse('user:login')


@pytest.mark.django_db
class TestUserLogin:
    """Class to test out the user login"""

    def test_user_url_succeeds(self):
        """Test the paths"""
        assert resolve(LOGIN_URL).view_name == 'user:login'

    def test_user_login_succeeds(self, client, create_user):
        """Test that users can login"""

        create_user(USER)

        response = client.post(LOGIN_URL, data={**USER})
        resp_data = response.data

        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert resp_data['user_message'] == MESSAGES['LOGIN']
        assert resp_data['data']['token'] is not None

    def test_user_login_authentication_fails(self, client):
        """Test that a user who is not registered cannot login."""

        response = client.post(LOGIN_URL, data=UNREGISTERED_USER)
        resp_data = response.data
        errors = resp_data['errors']
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['USR_O3']
        assert errors['error'][0] == ERRORS['USR_06']

    def test_user_login_with_blank_fields_fails(self, client):
        """Test that a user cannot login with blank variables"""

        response = client.post(LOGIN_URL, data=USER_INVALID)
        resp_data = response.data
        errors = resp_data['errors']
        assert response.status_code == 400
        assert resp_data['user_message'] == ERRORS['USR_O3']
        assert errors['email'][0] == ERRORS['USR_07']
        assert errors['password'][0] == ERRORS['USR_07']

    def test_user_login_no_data_fails(self, client):
        """Test that a user cannot login with no data"""

        response = client.post(LOGIN_URL, data={})
        resp_data = response.data
        errors = resp_data['errors']
        assert response.status_code == 400
        assert resp_data['user_message'] == ERRORS['USR_O3']
        assert errors['email'][0] == ERRORS['USR_04']
        assert errors['password'][0] == ERRORS['USR_04']

    def test_user_login_with_invalid_data_fails(self, client):
        """Test that users cannot register without invalid data"""

        response = client.post(LOGIN_URL,
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
