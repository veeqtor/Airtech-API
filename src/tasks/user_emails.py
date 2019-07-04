"""Module Sending emails to users"""

from django.contrib.auth import get_user_model
from django.template.loader import get_template

from src.services.email import send


class UserEmails:
    """class for sending out emails emails"""

    @classmethod
    def welcome_email(cls, user_id):
        """Sends out welcome email to users on registration.
        Args:
            user_id (str): User's id
        Returns:
            None
        """

        subject = 'Welcome to Airtech'
        found_user = cls.find_user(user_id)
        template = get_template('welcome_email.html')

        html_content = template.render()

        send.delay(subject, found_user.email, html_content)

    @classmethod
    def reservation_email(cls, user_id, reservation, context):
        """Sends out user reservation email.

        Args:
            user_id (str): User's id.
            context (object): Context object.
            reservation (object): Reservation object.

        Returns:
            None
        """

        subject = 'Reservation'
        found_user = cls.find_user(user_id)
        template = get_template('reservation_email.html')
        ctx = {
            'request': context,
            'reservation': cls.get_reservation(reservation)
        }

        html_content = template.render(ctx)

        send.delay(subject, found_user.email, html_content)

    @classmethod
    def find_user(cls, id):
        """Finds user from the database.
        Args:
            id (str): User id
        Returns:
            Object: The user object.
        """

        user = get_user_model()
        return user.objects.get(pk=id)

    @classmethod
    def get_reservation(cls, reservation):
        """Maps reservation data for email."""

        reservation_data = {
            'seat_number': reservation.seat_number,
            'seat_type': reservation.type,
            'plane': reservation.flight.plane.model,
            'flight_number': reservation.flight.flight_number,
            'date': reservation.flight.date,
            'departure_time': reservation.flight.departure_time,
            'arrival_time': reservation.flight.arrival_time,
            'display_name': reservation.made_by.user_profile.display_name,
        }
        return reservation_data
