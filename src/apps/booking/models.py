"""Booking models"""

from django.db import models

from src.apps.core.models import BaseAuditableModel
from src.apps.user.models import User
from src.apps.flight.models import Seats, Flight
from django.utils.translation import gettext_lazy as _


class Reservation(BaseAuditableModel):
    """
    Model representing the Plane table.
    """

    flight = models.ForeignKey(Flight,
                               related_name='reservation',
                               on_delete=models.CASCADE)
    seat_number = models.CharField(_('Seat number'), max_length=100)
    booked = models.BooleanField(_('Has been Booked'), default=False)
    type = models.CharField(_('Type'), max_length=20, choices=Seats.TYPE)
    made_by = models.ForeignKey(User,
                                related_name='reservation',
                                on_delete=models.CASCADE)
    date_made = models.DateTimeField(_('Date made'), auto_now_add=True)

    def __str__(self):
        return f'{self.flight} - {self.seat_number}'

    class Meta:
        """
        Meta class.
        """

        verbose_name_plural = "Reservations"
        db_table = "bo_reservations"


class Ticket(BaseAuditableModel):
    """
    Model representing the Ticket table.
    """

    ticket_ref = models.CharField(_('Ticket reference'), max_length=100)
    paid = models.BooleanField(_("Paid"), default=False)
    flight = models.ForeignKey(Flight,
                               related_name='ticket',
                               on_delete=models.CASCADE)
    seat_number = models.CharField(_('Seat number'), max_length=100)
    type = models.CharField(_('Type'), max_length=100, choices=Seats.TYPE)
    made_by = models.ForeignKey(User,
                                related_name='ticket',
                                on_delete=models.CASCADE)
    date_made = models.DateTimeField(_('Date made'), auto_now_add=True)

    def __str__(self):
        return f'{self.ticket_ref} - {self.seat_number}'

    class Meta:
        """
        Meta class.
        """

        verbose_name_plural = "Tickets"
        db_table = "bo_tickets"
