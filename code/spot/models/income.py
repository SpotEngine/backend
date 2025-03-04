from django.db import models
from utils.base_models import BaseModel, base_decimal
from django.db.transaction import atomic


class Income(BaseModel):
    trade = models.OneToOneField("Trade", on_delete=models.CASCADE, null=True, blank=True)
    token = models.ForeignKey("wallet.Token", on_delete=models.CASCADE, null=True, blank=True, related_name='spot_income')
    amount = base_decimal()
    
    @property
    def is_maker(self):
        return self.trade.is_maker
    
    @classmethod
    @atomic
    def create(cls, trade, token, amount):
        income = cls.objects.create(trade=trade, token=token, amount=amount)
        return income
