"""Module for pytest configs and fixtures"""
from datetime import date, timedelta
import datetime

import pytest
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils.six import BytesIO, StringIO
from PIL import Image

from rest_framework_jwt.settings import api_settings

from src.apps.user_profile.models import Passport
from src.apps.flight.models import Plane, Seats, Flight
from src.apps.booking.models import Reservation, Ticket
from src.apps.user.api.serializers import UserSerializer
from tests.fixtures.user import USER
from tests.fixtures.user_profile import NEW_PROFILE
from tests.fixtures.passport import NEW_PASSPORT
from tests.fixtures.plane import NEW_PLANE, SEATS

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@pytest.fixture(scope='function')
def create_user():
    """Fixture to create a new user"""

    def user(data):
        """
        create a user
        """
        return get_user_model().objects.create_user(**data)

    return user


@pytest.fixture(scope='function')
def create_superuser():
    """Fixture to create a user."""

    def super_user(data):
        """
        create a superuser
        """
        return get_user_model().objects.create_superuser(**data)

    return super_user


@pytest.fixture(scope='function')
def auth_header(client, create_user):
    """Authentication header"""

    user = create_user(USER)
    serializer = UserSerializer(user)
    payload = jwt_payload_handler(serializer.data)
    token = jwt_encode_handler(payload)

    return {'HTTP_AUTHORIZATION': f'Bearer {token}'}


@pytest.fixture(scope='function')
def generate_token(create_user):
    """Generates jwt token"""

    def token(user):
        """Wrapped func"""

        serializer = UserSerializer(user)
        payload = jwt_payload_handler(serializer.data)
        return jwt_encode_handler(payload)

    return token


@pytest.fixture(scope='function')
def create_profile(create_user):
    """Fixture to create a user profile."""

    user = create_user(USER)
    user_profile = user.user_profile

    for key, value in NEW_PROFILE.items():
        setattr(user_profile, key, value)
    user_profile.save()

    return user_profile


@pytest.fixture(scope='function')
def create_passport(create_profile):
    """Fixture to add passport."""

    profile = create_profile
    NEW_PASSPORT['profile'] = profile
    passport = Passport(**NEW_PASSPORT)

    return passport


@pytest.fixture(scope='function')
def add_passports(create_profile):
    """Fixture to more passports."""
    profile = create_profile

    passports = []
    for index in range(5):
        passport_copy = NEW_PASSPORT.copy()
        passport_copy['passport_number'] = f'A1234567{index}'
        passport_copy['profile'] = profile
        passports.append(passport_copy)

    return [Passport.objects.create(**passport) for passport in passports]


@pytest.fixture(scope='function')
def add_seats():
    """Fixture to add seats"""

    return [Seats.objects.create(**seat) for seat in SEATS]


@pytest.fixture(scope='function')
def add_planes(add_seats):
    """Fixture to add plane"""

    seats = add_seats
    planes = [Plane.objects.create(**plane) for plane in NEW_PLANE]

    for plane in planes:
        plane.seats.set(seats)
        plane.save()

    return planes


@pytest.fixture(scope='function')
def add_flights(add_planes):
    """Fixture to add flights"""

    flights = [{
        "flight_number": "FLI-0011",
        "plane": add_planes[0],
        "take_off": "LOS",
        "destination": "ATL",
        "price": 2300.34,
        "date": date.today() + timedelta(days=7),
        "departure_time": datetime.time(8, 10),
        "arrival_time": datetime.time(11, 15),
    }, {
        "flight_number": "FLI-0010",
        "plane": add_planes[1],
        "take_off": "LOS",
        "destination": "ATL",
        "price": 2300.34,
        "date": date.today() + timedelta(days=7),
        "departure_time": datetime.time(8, 10),
        "arrival_time": datetime.time(11, 15),
    }]

    return [Flight.objects.create(**flight) for flight in flights]


@pytest.fixture(scope='function')
def add_reservations(create_user, add_flights):
    """Fixture to add reservations"""

    user = create_user(USER)

    reservations = [{
        "flight": add_flights[0],
        "seat_number": "E001",
        "type": "ECO",
        "made_by": user,
    }, {
        "flight": add_flights[1],
        "seat_number": "E001",
        "type": "ECO",
        "made_by": user
    }]

    return [
        Reservation.objects.create(**reservation)
        for reservation in reservations
    ]


@pytest.fixture(scope='function')
def add_due_flights(add_planes):
    """Fixture to add flights"""

    flights = [{
        "flight_number": "FLI-0011",
        "plane": add_planes[0],
        "take_off": "LOS",
        "destination": "ATL",
        "price": 2300.34,
        "date": date.today() + timedelta(days=1),
        "departure_time": datetime.time(8, 10),
        "arrival_time": datetime.time(11, 15),
    }, {
        "flight_number": "FLI-0010",
        "plane": add_planes[1],
        "take_off": "LOS",
        "destination": "ATL",
        "price": 2300.34,
        "date": date.today() + timedelta(days=1),
        "departure_time": datetime.time(8, 10),
        "arrival_time": datetime.time(11, 15),
    }]

    return [Flight.objects.create(**flight) for flight in flights]


@pytest.fixture(scope='function')
def add_due_reservations(create_user, add_due_flights):
    """Fixture to add reservations"""

    user = create_user(USER)
    reservations = [{
        "flight": add_due_flights[0],
        "seat_number": "E001",
        "type": "ECO",
        "made_by": user,
    }, {
        "flight": add_due_flights[1],
        "seat_number": "E001",
        "type": "ECO",
        "made_by": user
    }]

    return [
        Reservation.objects.create(**reservation)
        for reservation in reservations
    ]


@pytest.fixture(scope='function')
def add_due_tickets(create_user, add_due_flights):
    """Fixture to add tickets"""

    user = create_user(USER)
    tickets = [{
        "ticket_ref": "LOS29203SLC",
        "paid": False,
        "flight": add_due_flights[0],
        "type": "ECO",
        "seat_number": "E001",
        "made_by": user,
    }, {
        "ticket_ref": "LOS24933SLC",
        "paid": False,
        "flight": add_due_flights[1],
        "type": "ECO",
        "seat_number": "E001",
        "made_by": user
    }]

    return [Ticket.objects.create(**ticket) for ticket in tickets]


@pytest.fixture(scope='function')
def add_tickets(create_user, add_flights):
    """Fixture to add tickets"""

    user = create_user(USER)
    tickets = [{
        "ticket_ref": "LOS29203SLC",
        "paid": False,
        "flight": add_flights[0],
        "type": "ECO",
        "seat_number": "E001",
        "made_by": user,
    }, {
        "ticket_ref": "LOS24933SLC",
        "paid": False,
        "flight": add_flights[1],
        "type": "ECO",
        "seat_number": "E001",
        "made_by": user
    }]

    return [Ticket.objects.create(**ticket) for ticket in tickets]


@pytest.fixture(scope='function')
def create_image():
    """Fixture to create image"""

    def create_image(storage,
                     filename,
                     size=(100, 100),
                     image_mode='RGB',
                     image_format='png'):
        """
        References: http://blog.cynthiakiser.com/blog/2016/06/26/testing-file
        -uploads-in-django/
        Generate a test image, returning the filename
        that it was saved as.

        If ``storage`` is ``None``, the BytesIO containing the image data
        will be passed instead.
        """
        data = BytesIO()
        Image.new(image_mode, size).save(data, image_format)
        data.seek(0)
        if not storage:
            return data
        image_file = ContentFile(data.read())
        return storage.save(filename, image_file)

    return create_image
