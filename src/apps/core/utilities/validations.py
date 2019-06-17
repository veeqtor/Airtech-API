"""Validations"""

# system imports
import re

# third party imports
from rest_framework import serializers
from src.apps.core.utilities.messages import ERRORS

# email regex
EMAIL_REGEX = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

# password regex
PASSWORD_REGEX = re.compile(
    r'(^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,15}$)'
)


def email_validation(data):
    """Validates the email"""

    if not EMAIL_REGEX.match(data):
        raise serializers.ValidationError(ERRORS['USR_01'])


def password_validation(data):
    """Validates the password"""

    if not PASSWORD_REGEX.match(data):
        raise serializers.ValidationError(ERRORS['USR_02'])
