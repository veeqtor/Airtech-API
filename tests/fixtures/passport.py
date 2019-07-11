"""Module for user passport fixtures"""

NEW_PASSPORT = {
    "passport_number": "A1039939",
    "country": "Ghana",
    "issued_date": "2019-03-12",
    "expiry_date": "2019-08-29"
}

EDIT_PASSPORT = {
    "country": "Ghana",
    "issued_date": "2019-03-25",
    "expiry_date": "2019-08-30"
}

INVALID_PASSPORT = {
    "country": "",
    "issued_date": "2019-03-25",
    "expiry_date": "2019-08-30"
}
