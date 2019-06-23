"""Test module for the plane endpoint"""

import pytest
from django.urls import resolve, reverse

from src.apps.core.utilities.messages import ERRORS
from tests.fixtures.plane import NEW_PLANE, SEATS
from tests.fixtures.user import USER

PLANE_URL = reverse('flight:plane-list')
GET_A_PLANE_URL = 'flight:plane-detail'


@pytest.mark.django_db
class TestPlaneView:
    """Class to test plane views"""

    def test_plane_url_succeeds(self):
        """Test the paths"""

        assert resolve(PLANE_URL).view_name == 'flight:plane-list'
        assert resolve(reverse('flight:plane-detail',
                               args=['pk'])).view_name == 'flight:plane-detail'

    def test_getting_all_plane_succeeds(self, auth_header, add_planes, client):
        """Test getting available plane."""

        response = client.get(PLANE_URL, **auth_header)
        resp_data = response.data
        data = resp_data['data']
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert len(data) == 2
        assert data[0]['model'] == str(NEW_PLANE[0]['model'])

    def test_getting_all_plane_without_auth_fails(self, client):
        """Test getting available planes fails"""

        response = client.get(PLANE_URL)
        resp_data = response.data
        assert response.status_code == 401
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['AUTH_01']

    def test_getting_a_plane_succeeds(self, client, auth_header, add_planes):
        """Test getting a plane."""

        plane = add_planes[0]
        plane_url = reverse(GET_A_PLANE_URL, args=[plane.id])

        response = client.get(plane_url, **auth_header)
        resp_data = response.data
        data = resp_data['data']
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert isinstance(data['seats'], list)
        assert data['model'] == plane.model

    def test_getting_a_plane_without_auth_fails(self, client, add_planes):
        """Test getting a plane fails"""

        plane = add_planes[0]
        plane_url = reverse(GET_A_PLANE_URL, args=[plane.id])

        response = client.get(plane_url)
        resp_data = response.data
        assert response.status_code == 401
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['AUTH_01']

    def test_getting_a_plane_with_invalid_pk_fails(self, client, auth_header):
        """Test getting a plane fails"""

        plane_url = reverse(GET_A_PLANE_URL, args=['invalid'])

        response = client.get(plane_url, **auth_header)
        resp_data = response.data
        assert response.status_code == 404
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['USR_09']

    def test_updating_a_plane_with_invalid_data_fails(
            self,
            client,
            add_planes,
            create_superuser,
            generate_token,
    ):
        """Test update flight with invalid data"""
        user = create_superuser(USER)
        token = generate_token(user)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        plane = add_planes[0]
        plane_url = reverse(GET_A_PLANE_URL, args=[plane.id])

        NEW_PLANE[0]['model'] = ''

        response = client.patch(plane_url,
                                content_type='application/json',
                                data=NEW_PLANE[0],
                                **auth_header)
        resp_data = response.data
        data = resp_data['errors']

        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert data['model'][0] == ERRORS['USR_07']

    def test_only_admin_can_update_a_plane_succeeds(self, client,
                                                    create_superuser,
                                                    generate_token,
                                                    add_planes):
        """Test that admin should be able to update plane"""

        user = create_superuser(USER)
        token = generate_token(user)
        plane = add_planes[1]
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        plane_url = reverse(GET_A_PLANE_URL, args=[plane.id])

        NEW_PLANE[1]['model'] = 'PT=JET'
        # NEW_PLANE[1]['seats'] = SEATS

        response = client.patch(plane_url,
                                content_type='application/json',
                                data=NEW_PLANE[1],
                                **auth_header)
        resp_data = response.data
        data = resp_data['data']

        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert data['model'] == NEW_PLANE[1]['model']

    def test_users_cannot_update_a_plane_fails(self, client, auth_header,
                                               add_planes):
        """Test that admin should be able to update flight"""
        plane = add_planes[1]
        plane_url = reverse(GET_A_PLANE_URL, args=[plane.id])

        NEW_PLANE[0]['model'] = 'EUT-123IR'

        response = client.patch(plane_url,
                                content_type='application/json',
                                data=NEW_PLANE[0],
                                **auth_header)
        resp_data = response.data
        assert response.status_code == 403
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['AUTH_02']

    def test_users_creating_a_plane_fails(self, client, auth_header):
        """Test that users should not be able to create plane"""

        NEW_PLANE[0]['seats'] = SEATS

        response = client.post(PLANE_URL,
                               content_type='application/json',
                               data=NEW_PLANE,
                               **auth_header)

        resp_data = response.data
        assert response.status_code == 403
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['AUTH_02']

    def test_only_admin_can_create_plane_succeed(self, client,
                                                 create_superuser,
                                                 generate_token):
        """Test that admin should be able to create plane"""
        user = create_superuser(USER)
        token = generate_token(user)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        NEW_PLANE[0]['seats'] = SEATS

        response = client.post(PLANE_URL,
                               content_type='application/json',
                               data=NEW_PLANE[0],
                               **auth_header)
        resp_data = response.data
        data = resp_data['data']
        assert response.status_code == 201
        assert resp_data['status'] == 'success'
        assert data['model'] == NEW_PLANE[0]['model']

    def test_creating_a_flight_with_invalid_data_fails(self, client,
                                                       create_superuser,
                                                       generate_token):
        """Test create flight with invalid data"""

        user = create_superuser(USER)
        token = generate_token(user)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        NEW_PLANE[0]['model'] = ''

        response = client.post(PLANE_URL,
                               content_type='application/json',
                               data=NEW_PLANE[0],
                               **auth_header)
        resp_data = response.data
        data = resp_data['errors']

        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert data['model'][0] == ERRORS['USR_07']

    def test_admin_can_update_plane_with_invalid_id_fails(
            self, client, create_superuser, generate_token):
        """Test that admin should not be able to update a plane with
        invalid param id"""

        user = create_superuser(USER)
        token = generate_token(user)
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        plane_url = reverse(GET_A_PLANE_URL, args=['invalid'])

        response = client.patch(plane_url,
                                content_type='application/json',
                                data=NEW_PLANE[0],
                                **auth_header)
        resp_data = response.data
        assert response.status_code == 404
        assert resp_data['status'] == 'error'
        assert resp_data['user_message'] == ERRORS['USR_09']
