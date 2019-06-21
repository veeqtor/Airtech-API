"""Admin"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


@admin.register(models.Plane)
class PlaneAdmin(admin.ModelAdmin):
    """custom admin for the plane model"""

    ordering = ['id']
    list_display = ['model', 'grounded', 'get_seats']
    list_per_page = 25

    fieldsets = ((_('Plane info'), {
        'fields': ('model', 'grounded', 'seats')
    }), )


@admin.register(models.Seats)
class SeatsAdmin(admin.ModelAdmin):
    """custom admin for the seats model"""

    ordering = ['type']
    list_display = ['type', 'number', 'booked', 'reserved']
    list_per_page = 25

    fieldsets = ((_('Seat info'), {
        'fields': ('type', 'number', 'booked', 'reserved')
    }), )


@admin.register(models.Flight)
class FlightAdmin(admin.ModelAdmin):
    """custom admin for the flights model"""

    ordering = ['flight_number', 'date']
    list_display = [
        'plane', 'flight_number', 'price', 'take_off', 'destination', 'date',
        'flight_duration', 'departure_time', 'arrival_time'
    ]
    list_display_links = ('plane', 'flight_number', 'price')

    list_per_page = 25

    fieldsets = ((_('Flight info'), {
        'fields': ('plane', 'flight_number', 'price', 'take_off',
                   'destination', 'date', 'departure_time', 'arrival_time')
    }), )
