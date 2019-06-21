"""Test module for the passport model"""

import pytest
from tests.fixtures.passport import NEW_PASSPORT

pytestmark = pytest.mark.django_db


class TestPassportModel:
    """Test passport model"""

    def test_the_model_string_succeeds(self, create_passport):
        """Test that passport model string rep is correct."""

        passport = create_passport
        assert passport.__str__(
        ) == f'{passport.passport_number} - {passport.country}'

    def test_passport_creation_succeeds(self, create_passport):
        """
        Test that a user passport model can be successfully created.
        """
        passport = create_passport

        assert passport.passport_number == NEW_PASSPORT['passport_number']
        assert passport.country == NEW_PASSPORT['country']
        assert passport.issued_date == NEW_PASSPORT['issued_date']
        assert passport.expiry_date == NEW_PASSPORT['expiry_date']

    def test_passport_deletion_succeeds(self, create_passport):
        """
        Test user passport deletion
        """

        passport = create_passport
        passport.delete()

        assert passport.deleted

    def test_passport_hard_deletion_succeeds(self, create_passport):
        """
        Test user passport hard deletion
        """

        passport = create_passport
        passport.hard_delete()

        assert passport.id is None
