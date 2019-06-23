"""Booking models"""

from django.db import models
from datetime import datetime, date

from src.apps.core.models import BaseAuditableModel
from src.apps.user.models import User
from django.utils.translation import gettext_lazy as _


class Reservation(BaseAuditableModel):
    """Model representing the Plane table"""

    flight_number = models.CharField(_('Flight number'), max_length=100)
    seat = models.CharField(_('Seat'), max_length=100)
    made_by = models.ForeignKey(User,
                                related_name='reservation',
                                on_delete=models.CASCADE)
    date_made = models.DateTimeField(_('Date made'), auto_now_add=True)

    def __str__(self):
        return f'{self.flight_number} - {self.seat}'

    class Meta:
        """Meta class"""

        verbose_name_plural = "Reservations"
        db_table = "bo_reservations"


class Ticket(BaseAuditableModel):
    """Model representing the Ticket table"""

    ticket_ref = models.CharField(_('Ticket reference'), max_length=100)
    paid = models.BooleanField(_("Paid"), default=False)
    flight_number = models.CharField(_('Flight number'), max_length=100)
    take_off = models.CharField(_('Take off'), max_length=100, null=True)
    destination = models.CharField(_('Destination'), max_length=100, null=True)
    seat = models.CharField(_('Seat'), max_length=100)
    date = models.DateField(_('Date'))
    departure_time = models.TimeField(_('Departure Time'))
    arrival_time = models.TimeField(_('Arrival Time'))
    made_by = models.ForeignKey(User,
                                related_name='ticket',
                                on_delete=models.CASCADE)
    date_made = models.DateTimeField(_('Date made'), auto_now_add=True)

    @property
    def flight_duration(self):
        """Flight duration"""

        duration = datetime.combine(date.min,
                                    self.arrival_time) - datetime.combine(
                                        date.min, self.departure_time)
        return duration

    def __str__(self):
        return f'{self.ticket_ref} - {self.seat}'

    class Meta:
        """Meta class"""

        verbose_name_plural = "Tickets"
        db_table = "bo_tickets"
