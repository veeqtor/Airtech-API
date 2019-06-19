"""User Profile"""

from django.db import models
from src.apps.core.models import BaseAuditableModel
from django.utils.translation import gettext_lazy as _

from src.apps.user.models import User


class UserProfile(BaseAuditableModel):
    """User profile model"""

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('None', 'None'),
    )

    SEATS = (('Window', 'Window seat'), ('Aisle', 'Aisle seat'))

    first_name = models.CharField(
        _('First Name'),
        max_length=255,
        null=True,
    )
    middle_name = models.CharField(
        _('Middle Name'),
        max_length=255,
        null=True,
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=255,
        null=True,
    )
    gender = models.CharField(
        _('Gender'),
        max_length=10,
        choices=GENDER,
        default=None,
        null=True,
    )
    phone = models.CharField(
        _('Phone number'),
        null=True,
        max_length=100,
    )

    dob = models.DateField(
        _('Date of Birth'),
        null=True,
    )
    seat_preference = models.CharField(_('Seat Preference'),
                                       max_length=10,
                                       choices=SEATS,
                                       default=None,
                                       null=True)
    user = models.OneToOneField(
        User,
        related_name='user_profile',
        on_delete=models.CASCADE,
    )

    @property
    def display_name(self) -> str:
        """Returns the display of the user"""

        return f'{self.first_name} {self.last_name}'

    class Meta:
        """Meta"""
        verbose_name_plural = 'User profiles'
        db_table = 'user_profiles'

    def __str__(self):
        """String representation"""

        return f'{self.display_name}'


class Passport(BaseAuditableModel):
    """Model for the passport table"""

    image = models.CharField(
        _('Passport Image URL'),
        max_length=255,
        null=True,
    )
    passport_number = models.CharField(_('Passport Number'),
                                       max_length=100,
                                       null=True,
                                       unique=True)
    country = models.CharField(_('Country of Citizenship'),
                               max_length=255,
                               null=True)
    issued_date = models.DateField(
        _('Issued date'),
        null=True,
    )
    expiry_date = models.DateField(
        _('Expiry date'),
        null=True,
    )

    profile = models.ForeignKey(
        UserProfile,
        related_name='passports',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta"""
        verbose_name_plural = 'Passports'
        db_table = 'user_passports'

    def __str__(self):
        """String representation"""

        return f'{self.passport_number} - {self.country}'
