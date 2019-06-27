"""User Serializer"""

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from src.apps.core.utilities.validations import (password_validation,
                                                 email_validation)
from src.apps.user_profile.api.serializers import UserProfileSerializer
from src.apps.core.utilities.messages import ERRORS

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
    """Class representing the User serializer"""

    class Meta:
        """Meta class"""

        model = get_user_model()
        fields = ['id', 'email', 'password', 'is_staff', 'is_superuser']
        read_only_fields = ['id', 'date_joined', 'is_staff', 'is_superuser']
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


class AuthTokenSerializer(JSONWebTokenSerializer):
    """Class representing the JWT Token Payload serializer"""

    def validate_password(self, attrs) -> str:
        """Validates the password"""

        password_validation(attrs)
        return attrs

    def validate_email(self, attrs) -> str:
        """Validates the password"""

        email_validation(attrs)
        return attrs

    def validate(self, attrs) -> dict:
        """Validate and authenticate the user"""

        request = self.context.get('request')

        credentials = {
            'username': attrs.get('email'),
            'password': attrs.get('password')
        }

        user = authenticate(request=request, **credentials)

        if user is not None and user.is_active:
            serializer = UserSerializer(user)
            payload = jwt_payload_handler(serializer.data)

            return {
                'token': jwt_encode_handler(payload),
            }
        else:
            raise serializers.ValidationError(ERRORS['USR_06'],
                                              code='authentication')


class UserFullNameSerializer(UserSerializer):
    """Serializer class for user's details"""

    user_profile = UserProfileSerializer(read_only=True)

    class Meta(UserSerializer.Meta):
        """Meta class"""

        fields = ['id', 'email', 'user_profile']
