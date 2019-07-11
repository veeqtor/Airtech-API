"""Signals for user profile"""

from src.apps.user_profile.models import UserProfile
from src.services.user_emails import UserEmails


class UserProfileSignals(object):
    """Signals for the user profile"""

    @staticmethod
    def create_profile(sender, instance, created, **kwargs):
        """
        Creates an empty profile when a user registers.
        """

        if created:
            profile = UserProfile(user=instance)
            profile.save()

    @staticmethod
    def welcome_email(sender, instance, created, **kwargs):
        """
        Sends out a welcome email.
        """

        if created:
            UserEmails.welcome_email(instance.pk)
