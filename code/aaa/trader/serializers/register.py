from rest_framework import serializers
from rest_registration.settings import registration_settings
from rest_registration.api.serializers import DefaultRegisterUserSerializer
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from ...models import Account
from utils.choices import AccountTypeChoice
from wallet.models import Asset



class UserRegister(DefaultRegisterUserSerializer):
    
    def validate_email(self, email):
        return email

    @atomic
    def save(self, **kwargs):
        kwargs['username'] = self.validated_data['email']
        user = super().save(**kwargs)
        account = Account.create(user=user, type=AccountTypeChoice.MAIN)
        Asset.fake_assets(account)
        return user

