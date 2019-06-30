"""User profile Serializers"""

from rest_framework import serializers
from src.apps.user_profile.models import UserProfile, Passport


class PassportSerializer(serializers.ModelSerializer):
    """Class representing the Passport serializer"""

    class Meta:
        """Meta class"""

        model = Passport

        fields = ('id', 'image', 'passport_number', 'country', 'issued_date',
                  'expiry_date')

    def create(self, validated_data):
        """Create new passport"""

        request = self.context.get('request')
        profile = request.user.user_profile

        validated_data['profile'] = profile
        instance = super(PassportSerializer, self).create(validated_data)

        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    """Class representing the User Profile serializer"""

    passports = PassportSerializer(many=True, read_only=True)

    class Meta:
        """Meta class"""

        model = UserProfile

        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'photo_url',
            'gender',
            'phone',
            'dob',
            'seat_preference',
            'passports',
        )
