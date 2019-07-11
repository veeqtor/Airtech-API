"""Test module for the user profile endpoint"""

import os
import pytest
from unittest.mock import Mock
from tempfile import NamedTemporaryFile

from django.urls import resolve, reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient
import cloudinary.uploader
from PIL import Image

from src.apps.core.utilities.messages import ERRORS, MESSAGES
from tests.fixtures.user_profile import (NEW_PROFILE, INVALID_PROFILE,
                                         MOCK_RESPONSE)

PROFILE_URL = reverse('user:profile')
PROFILE_PHOTO_URL = reverse('user:photo')
api_client = APIClient()


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

    def test_user_can_upload_profile_photo_succeeds(self, client, auth_header,
                                                    create_image):
        """Test that a user can upload profile photograph."""

        # Mock the cloudinary SDK
        cloudinary.uploader.upload = Mock(return_value=MOCK_RESPONSE)
        cloudinary.uploader.destroy = Mock()

        # set up form data
        profile_photo = create_image(None, 'photo_pic.png')
        photo_file = SimpleUploadedFile('test_photo.png',
                                        profile_photo.getvalue(),
                                        content_type='image/png')
        data = dict(photo=photo_file)
        response = api_client.put(PROFILE_PHOTO_URL,
                                  data=data,
                                  format="multipart",
                                  **auth_header)

        resp_data = response.data

        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert resp_data['user_message'] == MESSAGES['PHOTO_UPLOAD']
        assert resp_data['data'] == []
        assert cloudinary.uploader.upload.called
        assert cloudinary.uploader.upload.call_count == 1
        assert cloudinary.uploader.destroy.called
        assert cloudinary.uploader.destroy.call_count == 1

    def test_user_cannot_upload_profile_photo_of_invalid_type_fails(
            self, client, auth_header, create_image):
        """Test that a user cannot upload profile photograph invalild file
        type."""

        # set up form data
        profile_photo = create_image(None, 'photo_pic.png')
        photo_file = SimpleUploadedFile('test_photo.png',
                                        profile_photo.getvalue(),
                                        content_type='text/plain')
        data = dict(photo=photo_file)
        response = api_client.put(PROFILE_PHOTO_URL,
                                  data=data,
                                  format="multipart",
                                  **auth_header)

        resp_data = response.data
        data = resp_data['errors']

        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert data['photo'][0] == ERRORS['USR_11']

    def test_user_cannot_upload_profile_photo_with_invalid_file_fails(
            self, client, auth_header):
        """Test that a user cannot upload profile photograph without file"""

        response = api_client.put(PROFILE_PHOTO_URL,
                                  data={},
                                  format="multipart",
                                  **auth_header)

        resp_data = response.data
        data = resp_data['errors']

        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert data['photo'][0] == ERRORS['USR_04']

    def test_uploading_profile_photo_with_file_exceeding_max_size_fails(
            self, client, auth_header, create_image):
        """Test uploading profile photograph exceeding max 2mb"""

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = os.path.join(base_dir,
                                'fixtures/media/high_resoulution.jpg')
        image = Image.open(filename)
        picture = NamedTemporaryFile()
        image.save(picture, format="JPEG")

        picture.seek(0)
        response = api_client.put(PROFILE_PHOTO_URL,
                                  data={'photo': picture},
                                  format="multipart",
                                  **auth_header)

        resp_data = response.data
        data = resp_data['errors']
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert data['photo'][0] == ERRORS['USR_10']

    def test_the_exception_handler_succeeds(self, client, auth_header,
                                            create_image):
        """Raise exception on upload"""

        # Mock the cloudinary SDK
        cloudinary.uploader.upload = Mock(return_value=Exception('Test'))
        cloudinary.uploader.destroy = Mock()

        # set up form data
        profile_photo = create_image(None, 'photo_pic.png')
        photo_file = SimpleUploadedFile('test_photo.png',
                                        profile_photo.getvalue(),
                                        content_type='image/png')
        data = dict(photo=photo_file)
        response = api_client.put(PROFILE_PHOTO_URL,
                                  data=data,
                                  format="multipart",
                                  **auth_header)

        resp_data = response.data
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert resp_data['user_message'] == MESSAGES['PHOTO_UPLOAD']
        assert resp_data['data'] == []
        assert cloudinary.uploader.upload.called
        assert cloudinary.uploader.upload.call_count == 1
