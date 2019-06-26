"""Module for the bookings urls."""

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from src.apps.booking.api.views import ReservationsView, TicketView

router = SimpleRouter()
router.register(r'', ReservationsView, basename='reservation')

urlpatterns = [
    path('reserve/', include(router.urls), name='reservation'),
    path('ticket/', TicketView.as_view(), name='ticket'),
]
