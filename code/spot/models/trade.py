from django.db import models
from decimal import Decimal
from utils.base_models import BaseModel, base_decimal
from utils.choices import OrderStatusChoice, SpotOrderSideChoice, SpotOrderTypeChoice, OrderTimeInForceChoice
from wallet.models import Asset


class Trade(BaseModel):
    order = models.ForeignKey("Order", on_delete=models.PROTECT, null=True, blank=True)
    symbol = models.ForeignKey("Symbol", on_delete=models.PROTECT, null=True, blank=True, db_index=True)
    match_tag = models.CharField(default="", max_length=40, null=True, blank=True)
    price = base_decimal()
    quantity = base_decimal()

    paid_token = models.ForeignKey("wallet.Token", on_delete=models.PROTECT, null=True, blank=True, related_name='spot_paid')
    paid_amount = base_decimal()
    paid_rebate = base_decimal()

    received_token = models.ForeignKey("wallet.Token", on_delete=models.PROTECT, null=True, blank=True, related_name='spot_received')
    received_amount = base_decimal()
    received_fee = base_decimal()
    is_maker = models.BooleanField(default=False, null=True, blank=True)
    
    @property
    def side(self):
        return self.order.side 
    @classmethod
    def create(cls, order, symbol, price, quantity, paid_token, received_token, is_maker, match_tag):
        Trade = cls.objects.create(
            order=order,
            symbol=symbol,
            price=price,
            quantity=quantity, 
            paid_token=paid_token, 
            received_token=received_token, 
            is_maker=is_maker, 
            match_tag=match_tag
        )
        return Trade


