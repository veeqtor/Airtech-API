"""Module for pytest configs"""

import pytest
from django.contrib.auth import get_user_model


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
    """Fixture to create a user"""

    def super_user(data):
        """
        create a superuser
        """
        return get_user_model().objects.create_superuser(**data)

    return super_user
