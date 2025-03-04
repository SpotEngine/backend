from rest_registration.api.serializers import DefaultLoginSerializer
from rest_framework import serializers

class UserLogin(DefaultLoginSerializer):
    def validate(self, attrs):
        raise serializers.ValidationError("use token login")
