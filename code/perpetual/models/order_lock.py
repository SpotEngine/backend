from django.db import models
from utils.base_models import BaseModel, base_decimal
from utils.enums import ZERO


class OrderLock(BaseModel):
    account = models.ForeignKey("aaa.Account", on_delete=models.PROTECT, null=True, blank=True, related_name='perp_orderlock')
    asset = models.ForeignKey("PerpetualWallet", on_delete=models.CASCADE, null=True, blank=True)
    amount = base_decimal()
    position = models.ForeignKey("Position", on_delete=models.CASCADE, null=True, blank=True,)
    size = base_decimal()
    fee = base_decimal()

    class Meta:
        indexes = [
            models.Index(fields=['position',]),
        ]

    @classmethod
    def create(cls, account_id, asset=None, position=None, amount=ZERO, size=ZERO, fee=ZERO):
        locked = cls.objects.create(
            account_id=account_id,
            asset=asset,
            amount=amount,
            position=position,
            size=size,
            fee=fee,
        )
        return locked

