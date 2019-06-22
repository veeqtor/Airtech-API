"""Admin"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """custom admin for the plane model"""

    ordering = ['id']
    list_display = ['flight_number', 'seat', 'made_by', 'date_made']
    list_per_page = 25

    fieldsets = ((_('Plane info'), {
        'fields': ('flight_number', 'seat', 'made_by')
    }), )
