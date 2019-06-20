"""Admin"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


@admin.register(models.UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    """custom admin for the user profile model"""

    ordering = ['id']
    list_display = ['display_name']
    list_per_page = 25

    fieldsets = ((_('Personal info'), {
        'fields': ('first_name', 'middle_name', 'last_name', 'dob', 'gender',
                   'phone', 'seat_preference', 'user')
    }), )


@admin.register(models.Passport)
class PassportAdmin(admin.ModelAdmin):
    """custom admin for the user passport model"""

    ordering = ['id']
    list_display = ['passport_number', 'country']
    list_per_page = 25

    fieldsets = ((_('Passport info'), {
        'fields': ('image', 'passport_number', 'country', 'issued_date',
                   'expiry_date', 'profile')
    }), )
