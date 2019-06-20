"""Module for messages"""

MESSAGES = {
    'REGISTER': 'successfully registered.',
    'LOGIN': 'successfully logged in.',
    'PASSPORT': 'Added a new passport.',
}

ERRORS = {
    'USR_01': 'Enter a valid email address.',
    'USR_02': 'Password must be alphanumeric and must contain at least '
    'one special character.',
    'USR_O3': 'There is a problem with the values provided.',
    'USR_04': 'This field is required.',
    'USR_05': 'user with this Email already exists.',
    'USR_06': 'Could not authenticated with the provided credentials',
    'USR_07': 'This field may not be blank.',
    'USR_09': 'Sorry, We could not find what you are looking for.',
    'AUTH_01': 'Authentication credentials were not provided.',
    'CUST_01': '{} with this {} already exists.'
}
