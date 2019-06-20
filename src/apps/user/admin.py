"""Admin settings"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from . import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    """custom admin for the user model"""

    ordering = ['id']
    list_display = [
        'email', 'is_verified', 'date_joined', 'is_staff', 'is_superuser'
    ]
    list_per_page = 25
    list_filter = ('is_staff', 'is_active')
    filter_horizontal = []

    fieldsets = (
        (None, {
            'fields': ('email', 'password', 'is_verified')
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('email', 'password1', 'password2'),
    }), )


admin.site.unregister(Group)
