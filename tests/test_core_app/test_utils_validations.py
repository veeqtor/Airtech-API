"""Modules to test validations"""

import pytest
from src.apps.core.utilities.validations import email_validation, serializers, \
    password_validation


class TestValidations:
    """class to test the validations utils"""

    def test_email_validations_fails(self):
        """Test the email validations"""
        email = 'test_userexample.com'

        with pytest.raises(serializers.ValidationError) as excinfo:  # noqa:
            # F841
            email_validation(email)

    def test_password_validations_fails(self):
        """Test the password validations"""
        password = "password@#"

        with pytest.raises(serializers.ValidationError) as excinfo:  # noqa:
            # F841
            password_validation(password)
