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
    'for flight {}.',
    'PHOTO_UPLOAD':
    'Your request is being processed, You will receive an '
    'email shortly',
}

ERRORS = {
    'USR_01':
    'Enter a valid email address.',
    'USR_02':
    'Password must be alphanumeric and must contain at least '
    'one special character.',
    'USR_O3':
    'There is a problem with the fields provided.',
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
    'USR_10':
    'Image file must not exceed 2Mb.',
    'USR_11':
    'File is not an image.',
    'AUTH_01':
    'Authentication credentials were not provided.',
    'AUTH_02':
    'You do not have permission to perform this action.',
    'CUST_01':
    '{} with this {} already exists.',
    'FLI_01':
    'There is a problem with the fields provided, either '
    'the flight is not available or the seat has already '
    'been booked/reserved.',
    'FLI_02':
    'Sorry but you cannot modify/cancel your reservation/booking '
    f'{settings.FLIGHT_EDIT_ALLOWANCE_DAYS} days before the '
    'flight date.',
    'RES_01':
    'Invalid date format, should be in this format "YYYY-MM-DD".',
    'RES_02':
    'Date params is required.',
}

FILE_ERRORS = {
    'FILE_01': {
        'photo': [ERRORS['USR_04']]
    },
    'FILE_02': {
        'photo': [ERRORS['USR_10']]
    },
    'FILE_03': {
        'photo': [ERRORS['USR_11']]
    }
}
