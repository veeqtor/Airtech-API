"""Apps"""

from django.apps import AppConfig
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model


class UserConfig(AppConfig):
    """
    Application config
    """
    name = 'src.apps.user'

    def ready(self) -> None:
        """Imports the signals and connect when Django starts"""

        from src.apps.core.signals.user_profile import UserProfileSignals

        user = get_user_model()

        post_save.connect(UserProfileSignals.create_profile, sender=user)
