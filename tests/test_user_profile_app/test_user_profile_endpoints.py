"""Test module for the user profile endpoint"""

import pytest
from django.urls import resolve, reverse

from src.apps.core.utilities.messages import ERRORS
from tests.fixtures.user_profile import NEW_PROFILE, INVALID_PROFILE

PROFILE_URL = reverse('user:profile')


@pytest.mark.django_db
class TestUserProfileView:
    """Class to test the user profile views"""

    def test_profile_url_succeeds(self):
        """Test the paths"""

        assert resolve(PROFILE_URL).view_name == 'user:profile'

    def test_getting_a_logged_in_user_profile_succeeds(self, auth_header,
                                                       client):
        """Test getting logged in users profile"""

        response = client.get(PROFILE_URL, **auth_header)
        resp_data = response.data
        data = resp_data['data']

        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert data['first_name'] is None
        assert data['last_name'] is None
        assert data['middle_name'] is None
        assert data['gender'] is None
        assert data['phone'] is None
        assert data['seat_preference'] is None
        assert data['dob'] is None

    def test_getting_a_logged_in_user_profile_without_auth_fails(self, client):
        """Test getting logged in users profile"""

        response = client.get(PROFILE_URL)
        resp_data = response.data
        assert response.status_code == 401
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['AUTH_01']

    def test_updating_user_profile_succeeds(self, client, auth_header):
        """Test that logged in user can update profile"""

        response = client.patch(PROFILE_URL,
                                content_type='application/json',
                                data=NEW_PROFILE,
                                **auth_header)
        resp_data = response.data
        data = resp_data['data']
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert data['first_name'] == NEW_PROFILE['first_name']
        assert data['last_name'] == NEW_PROFILE['last_name']
        assert data['middle_name'] == NEW_PROFILE['middle_name']
        assert data['gender'] == NEW_PROFILE['gender']
        assert data['phone'] == NEW_PROFILE['phone']
        assert data['seat_preference'] == NEW_PROFILE['seat_preference']
        assert data['dob'] == NEW_PROFILE['dob']

    def test_updating_user_profile_with_invalid_data_fails(
            self, client, auth_header):
        """Test that logged in user cannot update profile with invalid data"""

        response = client.patch(PROFILE_URL,
                                content_type='application/json',
                                data=INVALID_PROFILE,
                                **auth_header)
        resp_data = response.data
        data = resp_data['errors']

        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert data['middle_name'][0] == ERRORS['USR_07']
        assert data['phone'][0] == ERRORS['USR_07']

    def test_updating_a_logged_in_user_profile_without_auth_fails(
            self, client):
        """Test getting logged in users profile"""

        response = client.patch(PROFILE_URL)
        resp_data = response.data
        assert response.status_code == 401
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['AUTH_01']
