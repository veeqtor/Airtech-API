"""Module for pytest configs and fixtures"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings

from src.apps.user_profile.models import Passport
from src.apps.flight.models import Plane, Seats
from src.apps.user.api.serializer import UserSerializer
from tests.fixtures.user import USER
from tests.fixtures.user_profile import NEW_PROFILE
from tests.fixtures.passport import NEW_PASSPORT
from tests.fixtures.plane import NEW_PLANE, SEATS

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@pytest.fixture(scope='function')
def create_user():
    """Fixture to create a new user"""

    def user(data):
        """
        create a user
        """
        return get_user_model().objects.create_user(**data)

    return user


@pytest.fixture(scope='function')
def create_superuser():
    """Fixture to create a user."""

    def super_user(data):
        """
        create a superuser
        """
        return get_user_model().objects.create_superuser(**data)

    return super_user


@pytest.fixture(scope='function')
def auth_header(client, create_user):
    """Authentication header"""

    user = create_user(USER)
    serializer = UserSerializer(user)
    payload = jwt_payload_handler(serializer.data)
    token = jwt_encode_handler(payload)

    return {'HTTP_AUTHORIZATION': f'Bearer {token}'}


@pytest.fixture(scope='function')
def generate_token(create_user):
    """Generates jwt token"""

    def token(user):
        """Wrapped func"""

        serializer = UserSerializer(user)
        payload = jwt_payload_handler(serializer.data)
        return jwt_encode_handler(payload)

    return token


@pytest.fixture(scope='function')
def create_profile(create_user):
    """Fixture to create a user profile."""

    user = create_user(USER)
    user_profile = user.user_profile

    for key, value in NEW_PROFILE.items():
        setattr(user_profile, key, value)
    user_profile.save()

    return user_profile


@pytest.fixture(scope='function')
def create_passport(create_profile):
    """Fixture to add passport."""

    profile = create_profile
    NEW_PASSPORT['profile'] = profile
    passport = Passport(**NEW_PASSPORT)

    return passport


@pytest.fixture(scope='function')
def add_passports(create_profile):
    """Fixture to more passports."""
    profile = create_profile

    passports = []
    for index in range(5):
        passport_copy = NEW_PASSPORT.copy()
        passport_copy['passport_number'] = f'A1234567{index}'
        passport_copy['profile'] = profile
        passports.append(passport_copy)

    return [Passport.objects.create(**passport) for passport in passports]


@pytest.fixture(scope='function')
def add_seats():
    """Fixture to add seats"""

    return [Seats.objects.create(**seat) for seat in SEATS]


@pytest.fixture(scope='function')
def add_planes(add_seats):
    """Fixture to add plane"""

    seats = add_seats
    planes = [Plane.objects.create(**plane) for plane in NEW_PLANE]

    for plane in planes:
        plane.seats.set(seats)
        plane.save()

    return planes
