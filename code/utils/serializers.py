from rest_framework import serializers
from django.db import models


class UserSerializer(serializers.Serializer):

    class Meta:
        abstract = True

    @property
    def user_id(self):
        _user_id = self.context['user_id']
        return _user_id

class AccountSerializer(serializers.Serializer):

    class Meta:
        abstract = True

    @property
    def account_id(self):
        _account_id = self.context['account_id']
        return _account_id


class ShortDecimalField(serializers.DecimalField):
    """Same as DecimalField but no trailing zeros."""
    def to_representation(self, value):
        return super().to_representation(value).rstrip('0').rstrip('.')


class CustomModelSerializer(serializers.ModelSerializer):
    serializer_field_mapping = {
        **serializers.ModelSerializer.serializer_field_mapping,
        models.DecimalField: ShortDecimalField,
    }
    class Meta:
        abstract = True


class CustomUserModelSerializer(UserSerializer, CustomModelSerializer):
    class Meta:
        abstract = True

class CustomAccountModelSerializer(AccountSerializer, CustomModelSerializer):
    class Meta:
        abstract = True


def make_fields(required_fields=[], read_only_fields=[], optional_fields=[]):
    extra_kwargs = {}
    for field in required_fields:
        extra_kwargs[field] = {'required': True,  "allow_null": False, }
    for field in read_only_fields:
        extra_kwargs[field] = {'read_only': True,}
    fields = required_fields + read_only_fields + optional_fields
    return fields, extra_kwargs