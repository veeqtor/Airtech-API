"""Module for flight fixtures"""

from datetime import date, timedelta
import datetime

NEW_FLIGHT = {
    "flight_number": "FLI-0010",
    "plane": "{}",
    "take_off": "LOS",
    "destination": "ATL",
    "price": 2300.34,
    "date": date.today() + timedelta(days=4),
    "departure_time": datetime.time(8, 10),
    "arrival_time": datetime.time(11, 15),
}

DURATION = datetime.datetime.combine(date.min, datetime.time(
    11, 15)) - datetime.datetime.combine(date.min, datetime.time(8, 10))
