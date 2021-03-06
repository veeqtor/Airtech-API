"""Module for user fixtures"""

USER = {
    'email': 'test_user@example.com',
    'password': 'Password@1234',
}

USER_INVALID = {'email': '', 'password': ''}

SUPERUSER = {
    'email': 'test_userII@example.com',
    'password': 'password1234',
}

UNREGISTERED_USER = {
    'email': 'unregistered@example1.com',
    'password': 'Password@1234'
}

TEST_AUTH_USER = {
    'email': 'test_auth_user@example.com',
    'password': 'Password@12345',
}
