"""User model"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

from src.apps.core.models import BaseModel


class UserManager(BaseUserManager):
    """Custom user manager"""

    def create_user(self, email, password=None, **extra_fields) -> object:
        """creates and saves a new user.

        Arguments:
            email (str): User email
            password (str): User Password (default: (None))

        Returns:
            Object: User object
        """

        if not email:
            raise ValueError(_('Users must have an email address'))

        extra_fields['id'] = uuid4()
        normalized_email = self.normalize_email(email)
        user = self.model(email=normalized_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields) -> object:
        """Creates and saves a new superuser.

        Returns:
            Object: User object
        """

        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    """Custom user model"""

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('None', 'None'),
    )

    SEATS = (('Window', 'Window seat'), ('Aisle', 'Aisle seat'))

    email = models.EmailField(_('Email'), max_length=255, unique=True)
    first_name = models.CharField(_('First Name'), max_length=255, blank=True)
    middle_name = models.CharField(_('Middle Name'),
                                   max_length=255,
                                   blank=True)
    last_name = models.CharField(_('Last Name'), max_length=255, blank=True)
    is_active = models.BooleanField(_('Is active'), default=True)
    is_staff = models.BooleanField(_('Is staff'), default=False)
    verification_token = models.CharField(_('verification token'),
                                          max_length=100,
                                          blank=True,
                                          null=True)
    password_reset = models.CharField(_('Password reset token'),
                                      max_length=100,
                                      blank=True,
                                      null=True)
    is_verified = models.BooleanField(_('Is verified'), default=False)
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)
    gender = models.CharField(_('Gender'),
                              max_length=10,
                              choices=GENDER,
                              default=None,
                              null=True)

    dob = models.DateField(_('Date of Birth'), null=True)
    seat_preference = models.CharField(_('Seat Preference'),
                                       max_length=10,
                                       choices=SEATS,
                                       default=None,
                                       null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    @property
    def display_name(self) -> str:
        """Returns the display of the user"""

        return f'{self.first_name} {self.last_name}'

    class Meta:
        """Meta"""
        db_table = 'users'
