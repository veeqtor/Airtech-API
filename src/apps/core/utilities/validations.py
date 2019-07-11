"""Validations"""

# system imports
import re
from datetime import datetime

# third party imports
from rest_framework import serializers
from src.apps.core.utilities.messages import ERRORS
from src.apps.core.utilities.response_utils import ResponseHandler

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


def date_validator(date=None):
    """validates the date format"""

    try:
        if date is None:
            ResponseHandler.raise_error({'date': ERRORS['RES_02']})
        date_obj = datetime.strptime(date, '%Y-%m-%d')

        return date_obj

    except ValueError:
        ResponseHandler.raise_error({'date': ERRORS['RES_01']})
