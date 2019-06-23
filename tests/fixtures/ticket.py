"""Fixture for adding a new ticket."""
from datetime import date, timedelta
import datetime

NEW_TICKET = [{
    "ticket_ref": "LOS29203SLC",
    "paid": False,
    "flight_number": "",
    "take_off": "LOS",
    "destination": "SLC",
    "seat": "",
    "date": date.today() + timedelta(days=5),
    "departure_time": datetime.time(10, 10),
    "arrival_time": datetime.time(22, 15),
    "made_by": "",
}, {
    "ticket_ref": "LOS24933SLC",
    "paid": False,
    "flight_number": "",
    "take_off": "SLC",
    "destination": "LOS",
    "seat": "",
    "date": date.today() + timedelta(days=5),
    "departure_time": datetime.time(8, 10),
    "arrival_time": datetime.time(11, 15),
    "made_by": ""
}]

DURATION = datetime.datetime.combine(date.min, datetime.time(
    22, 15)) - datetime.datetime.combine(date.min, datetime.time(10, 10))
