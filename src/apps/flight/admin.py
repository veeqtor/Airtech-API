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
