"""Module for user profile fixtures"""

NEW_PROFILE = {
    "first_name": "Test",
    "middle_name": "User",
    "last_name": "Last",
    "gender": "M",
    "phone": "9415386941",
    "seat_preference": "Window",
    "dob": "2010-10-10"
}

INVALID_PROFILE = {
    "middle_name": "",
    "last_name": "Last",
    "gender": "M",
    "phone": "",
    "seat_preference": "Window",
}
