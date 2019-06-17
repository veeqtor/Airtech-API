"""User Serializer"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from src.apps.core.utilities.validations import (password_validation,
                                                 email_validation)


class UserSerializer(serializers.ModelSerializer):
    """Class representing the User serializer"""

    class Meta:
        """Meta class"""

        model = get_user_model()
        fields = [
            'id', 'email', 'password', 'last_name', 'first_name', 'is_staff',
            'is_superuser'
        ]
        read_only_fields = [
            'display_name', 'id', 'date_joined', 'is_staff', 'is_superuser'
        ]
        extra_kwargs = {
            'verification_token': {
                'write_only': True
            },
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def validate_password(self, attrs):
        """Validates the password"""

        password_validation(attrs)
        return attrs

    def validate_email(self, attrs):
        """Validates the password"""

        email_validation(attrs)
        return attrs

    def create(self, validated_data):
        """create a new user"""

        return get_user_model().objects.create_user(**validated_data)

    # def update(self, instance, validated_data):
    #     """Edit the user object"""
    #
    #     password = validated_data.pop('password')
    #     user = super().update(instance, validated_data)
    #     if password:
    #         user.set_password(password)
    #         user.save()
    #     return user
