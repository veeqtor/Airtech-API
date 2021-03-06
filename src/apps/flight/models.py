"""Flight models"""
from datetime import datetime, date
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
    seat_number = models.CharField(_('Seat number'), max_length=10)

    def __str__(self):
        return f'{self.type} - {self.seat_number}'

    class Meta:
        """Meta class"""

        verbose_name_plural = "Plane seats"
        db_table = "fl_seats"


class Plane(BaseAuditableModel):
    """Model representing the Plane table"""

    model = models.CharField(_('Plane model'), max_length=100, null=False)
    grounded = models.BooleanField(_('Is Grounded'), default=False)
    seats = models.ManyToManyField(Seats, related_name="plane")

    @property
    def get_seats(self):
        """Get all seats"""

        return "\n".join(
            [seat.seat_number for seat in self.seats.order_by('type')])

    def __str__(self):
        return self.model

    class Meta:
        """Meta class"""

        verbose_name_plural = "Planes"
        db_table = "fl_planes"


class Flight(BaseAuditableModel):
    """Model representing the Flight table"""

    STATUS = (
        ('Pending', 'Pending'),
        ('Departed', 'Departed'),
        ('Ready', 'Ready to leave'),
    )

    plane = models.ForeignKey(Plane,
                              related_name="flight",
                              on_delete=models.CASCADE)

    flight_number = models.CharField(_('Flight number'),
                                     max_length=100,
                                     unique=True,
                                     null=False)
    price = models.DecimalField(_('Price'), max_digits=11, decimal_places=2)
    take_off = models.CharField(_('Take off'), max_length=100, null=False)
    status = models.CharField(_('Status'),
                              max_length=100,
                              choices=STATUS,
                              default='Pending')
    destination = models.CharField(_('Destination'),
                                   max_length=100,
                                   null=False)
    date = models.DateField(_('Date'))
    departure_time = models.TimeField(_('Departure Time'))
    arrival_time = models.TimeField(_('Arrival Time'))

    @property
    def flight_duration(self):
        """Flight duration"""

        duration = datetime.combine(date.min,
                                    self.arrival_time) - datetime.combine(
                                        date.min, self.departure_time)
        return str(duration)

    def __str__(self):
        return f'{self.flight_number} - {self.take_off} to {self.destination}'

    class Meta:
        """Meta class"""

        verbose_name_plural = "Flights"
        db_table = "fl_flights"
