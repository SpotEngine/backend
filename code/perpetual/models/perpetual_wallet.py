from django.db.transaction import atomic
from django.db import models
from utils.base_models import BaseModel, base_decimal
from utils.helper import DecimalRound


class PerpetualWallet(BaseModel):
    account = models.ForeignKey('aaa.Account', on_delete=models.PROTECT, null=True, blank=True)
    token = models.ForeignKey('wallet.Token', on_delete=models.PROTECT, null=True, blank=True)
    # no locked amount: we use orders locked quantity for locking free
    free = base_decimal()

    class Meta:
        unique_together = ('account', 'token',)
        indexes = [
            models.Index(fields=['account', 'token'])
        ]

    def __str__(self):
        return f"{self.account_id}"
    
    @classmethod
    def create(cls, account, token):
        asset, _ = cls.objects.get_or_create(account=account, token=token)
        asset.save()
        return asset

    @classmethod
    def validate_and_lock_balance(cls, account_id, token, amount, exception):
        amount = DecimalRound.round_up(amount)
        asset, _ = cls.objects.select_for_update().get_or_create(account_id=account_id, token=token)
        if asset.free < amount:
            raise exception("insufficient account balance")
        asset.free -= amount
        asset.save()
        return asset

    @classmethod
    @atomic
    def add_to_asset(cls, account, token, quantity):
        asset = cls.create(account=account, token=token)
        asset = cls.objects.select_for_update().get(pk=asset.id)
        asset.free += quantity.normalize()
        asset.save()
        return asset