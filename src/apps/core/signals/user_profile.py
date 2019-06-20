"""Signals for user profile"""

from src.apps.user_profile.models import UserProfile


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
