from django.db import models
from utils.base_models import BaseModel, base_decimal


class Symbol(BaseModel):
    account = models.ForeignKey("aaa.Account", on_delete=models.PROTECT, null=True, blank=True)
    symbol = models.CharField(max_length=15, primary_key=True, unique=True)
    base = models.ForeignKey("wallet.Token", on_delete=models.PROTECT, null=True, blank=True, related_name="base")
    quote = models.ForeignKey("wallet.Token", on_delete=models.PROTECT, null=True, blank=True, related_name="quote")
    
    # status = models.CharField(default=SymbolStatusChoice.ACTIVE,  choices=SymbolStatusChoice.choices, max_length=20, null=True, blank=True)

    lot_size = base_decimal()
    tick_size = base_decimal()
    priority = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['priority']
        unique_together = ('base', 'quote',)
        

    def __str__(self):
        return self.symbol
    
    def save(self, *args, **kwargs) -> None:
        self.symbol = f"{self.base.ticker}{self.quote.ticker}"
        return super().save(*args, **kwargs)

    @classmethod
    def create(cls, account_id, base, quote, lot_size, tick_size):
        symbol = cls.objects.create(account_id=account_id, base=base, quote=quote, lot_size=lot_size, tick_size=tick_size)
        return symbol
    