"""Module to generate random token verification key"""

import secrets
import binascii
from datetime import datetime, timedelta
from src.apps.core.utilities.constants import CHARSETS


def generate_verification_token(exp=5):
    """Generates the verification token.

    Args:
        exp (int): The expiration time in minutes
    Returns:
        String: Token string
    """
    rand = secrets.token_urlsafe(16)
    rand_ii = secrets.token_urlsafe(16)
    date = datetime.now() + timedelta(minutes=exp)
    date_timestamp = str(round(date.timestamp())).encode(CHARSETS[1])
    encoded_timestamp = binascii.hexlify(date_timestamp).decode(CHARSETS[1])
    token = rand + encoded_timestamp + rand_ii

    return token


def is_valid(token):
    """Checks if the token is valid.

    Args:
        token (str): Token
    Returns:
        Boolean: True or false
    """
    if len(token) < 64:
        return False

    now = datetime.now().timestamp()
    time = token[22:][:20]
    decode_timstamp = binascii.unhexlify(time).decode(CHARSETS[1])

    if now > int(decode_timstamp):
        return False
    else:
        return True
