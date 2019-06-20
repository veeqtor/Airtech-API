"""Module for pytest configs and fixtures"""

import pytest
from django.contrib.auth import get_user_model

from src.apps.user_profile.models import Passport
from src.apps.user.api.serializer import UserSerializer
from tests.fixtures.user import USER
from tests.fixtures.user_profile import NEW_PROFILE
from tests.fixtures.passport import NEW_PASSPORT
from rest_framework_jwt.settings import api_settings

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
    passports = [{
        "image": "https://passport.usi.com",
        "passport_number": "A1039924",
        "country": "Ghana",
        "issued_date": "2019-03-12",
        "expiry_date": "2019-08-29",
        "profile": profile
    }, {
        "image": "https://passport.usi.com",
        "passport_number": "A1039908",
        "country": "Senegal",
        "issued_date": "2019-03-12",
        "expiry_date": "2019-08-29",
        "profile": profile
    }, {
        "image": "https://passport.usi.com",
        "passport_number": "A1039939",
        "country": "Nigeria",
        "issued_date": "2019-03-12",
        "expiry_date": "2019-08-29",
        "profile": profile
    }]
    return [Passport.objects.create(**passport) for passport in passports]
