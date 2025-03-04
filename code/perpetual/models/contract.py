from django.db import models
from utils.base_models import BaseModel, base_decimal, Decimal

class Contract(BaseModel):
    symbol = models.CharField(max_length=15, primary_key=True, unique=True)
    base = models.CharField(default='', max_length=10, null=True, blank=True)
    quote = models.ForeignKey("wallet.Token", on_delete=models.PROTECT, null=True, blank=True, related_name='prep_quote')
    
    margin = models.ForeignKey("wallet.Token", on_delete=models.PROTECT, null=True, blank=True, related_name='perp_margin')
    margin_amount = base_decimal()
    lot_size = base_decimal()
    max_size = base_decimal()
    tick_size = base_decimal()
    max_leverage = models.IntegerField(default=10, null=True, blank=True)
    priority = models.IntegerField(default=0, null=True, blank=True)
    liquidation_threshold = base_decimal(default=Decimal("0.02"))

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.symbol

    def save(self, *args, **kwargs) -> None:
        self.symbol = f"{self.base.upper()}{self.quote.ticker}"
        return super().save(*args, **kwargs)

    @classmethod
    def create(cls, base, quote, lot_size, tick_size, max_size):
        base = base.upper()
        contract, _ = cls.objects.get_or_create(base=base, quote=quote, defaults={
            'lot_size': lot_size, 
            'tick_size': tick_size,
            'max_leverage': 50,
            'max_size': max_size,
        })
        return contract