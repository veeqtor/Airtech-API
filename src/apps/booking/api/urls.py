"""Module for the bookings urls."""

from rest_framework.routers import SimpleRouter
from src.apps.booking.api.views import ReservationsViewSet, TicketViewSet

router = SimpleRouter()
router.register(r'reservations', ReservationsViewSet, basename='reservation')
router.register(r'ticket', TicketViewSet, basename='ticket')

urlpatterns = router.urls
