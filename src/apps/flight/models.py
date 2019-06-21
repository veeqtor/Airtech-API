"""Flight models"""

from django.db import models

from src.apps.core.models import BaseAuditableModel
from django.utils.translation import gettext_lazy as _


class Seats(BaseAuditableModel):
    """Model representing the Plane table"""

    TYPE = (
        ('ECO', 'Economy class'),
        ('BUS', 'Business class'),
    )

    type = models.CharField(_('Seat type'), max_length=20, choices=TYPE)
    booked = models.BooleanField(_('Is booked'), default=False)
    reserved = models.BooleanField(_('Is reserved'), default=False)
    number = models.CharField(_('Seat number'), max_length=10)

    def __str__(self):
        return f'{self.type} - {self.number}'

    class Meta:
        """Meta class"""

        verbose_name_plural = "Plane seats"
        db_table = "fl_seats"


class Plane(BaseAuditableModel):
    """Model representing the Plane table"""

    model = models.CharField(_('Plane model'), max_length=100, null=True)
    grounded = models.BooleanField(_('Is Grounded'), default=False)
    seats = models.ManyToManyField(Seats, related_name="plane")

    @property
    def get_seats(self):
        """Get all seats"""

        return "\n".join([seat.number for seat in self.seats.order_by('type')])

    def __str__(self):
        return self.model

    class Meta:
        """Meta class"""

        verbose_name_plural = "Planes"
        db_table = "fl_planes"
