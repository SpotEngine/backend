from django.db import models
from django.db.transaction import atomic
from utils.base_models import BaseModel, base_decimal, Decimal

class Asset(BaseModel):
    account = models.ForeignKey('aaa.Account', on_delete=models.PROTECT, null=True, blank=True)
    token = models.ForeignKey('Token', on_delete=models.PROTECT, null=True, blank=True)
    # no locked amount: we use orders locked quantity for locking balance
    free = base_decimal()
    # locked = base_decimal()


    class Meta:
        unique_together = ('account', 'token',)
        indexes = [
            models.Index(fields=['account', 'token'])
        ]

    def __str__(self):
        return f"{self.id}:{self.token.ticker}"

    @classmethod
    def fake_assets(cls, account):
        from wallet.models import Token
        # Crypto assets
        # usdt = Token.objects.get(ticker="USDT")
        # btc = Token.objects.get(ticker="BTC")
        # cls.add_to_asset(account, usdt, Decimal("100_000"))
        # cls.add_to_asset(account, btc, Decimal("1"))

        # FX assets
        usd = Token.objects.get(ticker="USD")
        eur = Token.objects.get(ticker="EUR")
        cls.add_to_asset(account, usd, Decimal("100_000"))
        cls.add_to_asset(account, eur, Decimal("100_000"))



    @classmethod
    def create(cls, account, token):
        asset, _ = cls.objects.get_or_create(account=account, token=token)
        asset.save()
        return asset
    

    @classmethod
    def validate_and_lock_balance(cls, account_id, token, amount, exception):
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