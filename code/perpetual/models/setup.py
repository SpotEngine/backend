from django.db import models
from decimal import Decimal
from utils.base_models import BaseModel, base_decimal
from utils.choices import MarginModeChoice, PositionModeChoice


class Setup(BaseModel):
    account = models.ForeignKey("aaa.Account", on_delete=models.PROTECT, null=True, blank=True)
    contract = models.ForeignKey("Contract", on_delete=models.PROTECT, null=True, blank=True)
    margin = models.CharField(default=MarginModeChoice.ISOLATED, max_length=20, choices=MarginModeChoice.choices, null=True, blank=True)
    mode = models.CharField(default=PositionModeChoice.ONEWAY, max_length=20, choices=PositionModeChoice.choices, null=True, blank=True)
    leverage = models.IntegerField(default=10, null=True, blank=True)    
    
    class Meta:
        unique_together = ('account', 'contract',)

    @classmethod
    def get_account_setup(cls, account_id, contract):
        setup, _ = cls.objects.get_or_create(account_id=account_id, contract=contract)
        return setup