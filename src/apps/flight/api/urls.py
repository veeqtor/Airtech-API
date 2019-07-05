"""Module for urls for the flight API"""

from rest_framework.routers import SimpleRouter

from src.apps.flight.api.views import FlightViewSet, PlaneView

router = SimpleRouter()
router.register(r'plane', PlaneView, basename='plane')
router.register(r'', FlightViewSet, basename='flight')
urlpatterns = router.urls
