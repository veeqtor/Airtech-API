"""Booking models"""

from django.db import models

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
        db_table = "fl_reservations"
