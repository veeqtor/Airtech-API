"""Test module for the user profile model"""

import pytest
from tests.fixtures.user import USER
from tests.fixtures.user_profile import NEW_PROFILE

pytestmark = pytest.mark.django_db


class TestUserProfileModel:
    """
    Test user profile model.
    """

    def test_the_model_string_succeeds(self, create_profile):
        """Test that vendors model string rep is correct."""

        profile = create_profile
        assert profile.__str__() == profile.display_name

    def test_user_profile_creation_succeeds(self, create_user):
        """
        Test that a user profile can be successfully created.
        """

        user = create_user(USER)
        assert isinstance(user.user_profile, object)

    def test_user_profile_modification_succeeds(self, create_profile):
        """
        Test that a user profile can be successfully created.
        """

        profile = create_profile
        assert profile.first_name == NEW_PROFILE['first_name']
        assert profile.last_name == NEW_PROFILE['last_name']
        assert profile.middle_name == NEW_PROFILE['middle_name']
        assert profile.gender == NEW_PROFILE['gender']
        assert profile.phone == NEW_PROFILE['phone']
        assert profile.seat_preference == NEW_PROFILE['seat_preference']
        assert profile.dob == NEW_PROFILE['dob']

    def test_user_profile_deletion_succeeds(self, create_profile):
        """
        Test that a user profile can be successfully deleted.
        """

        profile = create_profile
        profile.delete()

        assert profile.deleted

    def test_user_profile_hard_deletion_succeeds(self, create_profile):
        """
        Test that a user profile can be successfully hard deleted.
        """

        profile = create_profile
        profile.hard_delete()

        assert profile.id is None
