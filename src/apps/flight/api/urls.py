"""Module for urls for the flight API"""

from django.urls import path, include  # noqa: F401
from rest_framework.routers import SimpleRouter, DefaultRouter

from src.apps.flight.api.views import FlightViewSet, PlaneView

router = SimpleRouter()
router.register(r'plane', PlaneView, basename='plane')
router.register(r'', FlightViewSet, basename='flight')
urlpatterns = router.urls
