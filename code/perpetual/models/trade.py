from django.db import models
from utils.base_models import BaseModel, base_decimal


class Trade(BaseModel):
    order = models.ForeignKey("Order", on_delete=models.PROTECT, null=True, blank=True)
    contract = models.ForeignKey("Contract", on_delete=models.PROTECT, null=True, blank=True, db_index=True)
    match_tag = models.CharField(default="", max_length=40, null=True, blank=True)
    price = base_decimal()
    size = base_decimal()

    paid_token = models.ForeignKey("wallet.Token", on_delete=models.PROTECT, null=True, blank=True, related_name='perp_paid')
    paid_amount = base_decimal()
    received_amount = base_decimal()
    received_rebate = base_decimal()
    paid_fee = base_decimal()

    is_maker = models.BooleanField(default=False, null=True, blank=True)
    
    
    @classmethod
    def create(cls, order, contract, price, size, paid_token, is_maker, match_tag):
        Trade = cls.objects.create(
            order=order,
            contract=contract,
            price=price,
            size=size, 
            paid_token=paid_token, 
            is_maker=is_maker,
            match_tag=match_tag,
        )
        return Trade


