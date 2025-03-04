from django.db.transaction import atomic
from django.db import models
from utils.base_models import BaseModel
from .asset import Asset
from decimal import Decimal


class Token(BaseModel):
    account = models.ForeignKey("aaa.Account", on_delete=models.PROTECT, null=True, blank=True)
    ticker = models.CharField(max_length=10, primary_key=True, unique=True)
    name = models.CharField(default="", max_length=40, null=True, blank=True)
    supply = models.PositiveBigIntegerField(default=1, null=True, blank=True)
    is_transferable = models.BooleanField(default=True, null=True, blank=True)
    is_withdrawable = models.BooleanField(default=False, null=True, blank=True)
    priority = models.IntegerField(default=10, null=True, blank=True)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.ticker
    @property
    def info(self):
        return self.address
    
    def save(self, *args, **kwargs):
        self.ticker = self.ticker.upper()
        return super().save(*args, **kwargs)

    @classmethod
    @atomic
    def create(cls, account_id, ticker, name, supply):
        token = cls.objects.create(account_id=account_id, ticker=ticker, name=name, is_transferable=True, supply=supply)
        Asset.add_to_asset(account=token.account, token=token, quantity=Decimal(str(token.supply)))
        return token

