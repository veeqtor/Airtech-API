"""Module for messages"""
from django.conf import settings

MESSAGES = {
    'REGISTER':
    'successfully registered.',
    'LOGIN':
    'successfully logged in.',
    'PASSPORT':
    'Added a new passport.',
    'PLANE':
    'Added a new plane.',
    'FLIGHT':
    'Added a new flight.',
    'RESERVED':
    'Seat {} on flight {} has been successfully reserved for you.',
    'BOOKED':
    'Seat {} on flight {} has been successfully booked for you.',
    'RESERVE_CANCEL':
    'You have successfully cancelled your reservation ',
    'TICKET_CANCEL':
    'You have successfully cancelled your ticket '
    'for flight {}.'
}

ERRORS = {
    'USR_01':
    'Enter a valid email address.',
    'USR_02':
    'Password must be alphanumeric and must contain at least '
    'one special character.',
    'USR_O3':
    'There is a problem with the values provided.',
    'USR_04':
    'This field is required.',
    'USR_05':
    'user with this Email already exists.',
    'USR_06':
    'Could not authenticated with the provided credentials',
    'USR_07':
    'This field may not be blank.',
    'USR_09':
    'Sorry, We could not find what you are looking for.',
    'AUTH_01':
    'Authentication credentials were not provided.',
    'AUTH_02':
    'You do not have permission to perform this action.',
    'CUST_01':
    '{} with this {} already exists.',
    'FLI_01':
    'There is a problem with the values provided, either '
    'the flight is not available or the seat has already '
    'been booked/reserved.',
    'FLI_02':
    'Sorry but you cannot modify/cancel your reservation/booking '
    f'{settings.FLIGHT_EDIT_ALLOWANCE_DAYS} days before the '
    'flight date.'
}
