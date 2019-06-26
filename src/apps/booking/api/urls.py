"""Module for the bookings urls."""

from django.urls import path, include
from src.apps.booking.api.views import ReservationsView, TicketView

urlpatterns = [
    path('reserve/', ReservationsView.as_view(), name='reservation'),
    path('ticket/', TicketView.as_view(), name='ticket'),
]
