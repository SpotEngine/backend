from django.db import models
from decimal import Decimal
from utils.base_models import BaseModel, base_decimal
from utils.choices import OrderStatusChoice, SpotOrderSideChoice, SpotOrderTypeChoice, OrderTimeInForceChoice


class Order(BaseModel):
    account = models.ForeignKey("aaa.Account", on_delete=models.PROTECT, null=True, blank=True, related_name='spot_order')
    symbol = models.ForeignKey("Symbol", on_delete=models.PROTECT, null=True, blank=True)
    client_order_id = models.CharField(unique=True, max_length=40,)
    
    status = models.CharField(default=OrderStatusChoice.RECEIVED, max_length=15, choices=OrderStatusChoice.choices, null=True, blank=True)
    side = models.CharField(default=SpotOrderSideChoice.BUY, max_length=5, choices=SpotOrderSideChoice.choices, null=True, blank=True)
    type = models.CharField(default=SpotOrderTypeChoice.LIMIT, max_length=20, choices=SpotOrderTypeChoice.choices, null=True, blank=True)
    time_in_force = models.CharField(default=OrderTimeInForceChoice.GTC, max_length=5, choices=OrderTimeInForceChoice.choices, null=True, blank=True)
    
    price = base_decimal()
    quantity = base_decimal()
    filled_quantity = base_decimal()

    quote_quantity = base_decimal()
    filled_quote_quantity = base_decimal()

    locked_asset = models.ForeignKey("wallet.Asset", on_delete=models.PROTECT, null=True, blank=True)
    locked_amount = base_decimal()
    post_only = models.BooleanField(default=False, null=True, blank=True)
    fee_rebate = base_decimal(non_negative=False)

    class Meta:
        indexes = [
            models.Index(fields=['side', 'price',]),
        ]

    def __str__(self):
        return f"{self.id}:{self.side}"
    @classmethod
    def create_base_order(cls, account_id, client_order_id, symbol, locked_asset, locked_amount, side, type, fee_rebate, **kwargs):
        order = cls.objects.create(
            account_id=account_id,
            client_order_id=client_order_id,
            symbol=symbol,
            side=side,
            type=type,            
            locked_asset=locked_asset,
            locked_amount=locked_amount,
            fee_rebate=fee_rebate,
            **kwargs
        )
        return order

    @classmethod
    def create_market_buy_order(cls, account_id, client_order_id, symbol, quote_quantity, locked_asset, locked_amount, fee_rebate):
        kwargs = {
            "quote_quantity": quote_quantity,
        }
        order = cls.create_base_order(
            account_id=account_id,
            client_order_id=client_order_id,
            symbol=symbol,
            side=SpotOrderSideChoice.BUY,
            type=SpotOrderTypeChoice.MARKET,
            locked_asset=locked_asset,
            locked_amount=locked_amount,
            fee_rebate=fee_rebate,
            **kwargs
        )
        return order      


    @classmethod
    def create_market_sell_order(cls, account_id, client_order_id, symbol, quantity, locked_asset, locked_amount, fee_rebate):
        kwargs = {
            "quantity": quantity,
        }
        order = cls.create_base_order(
            account_id=account_id,
            client_order_id=client_order_id,
            symbol=symbol,
            side=SpotOrderSideChoice.SELL,
            type=SpotOrderTypeChoice.MARKET,
            locked_asset=locked_asset,
            locked_amount=locked_amount,
            fee_rebate=fee_rebate,
            **kwargs
        )
        return order      

    @classmethod
    def create_limit_order(cls, account_id, client_order_id, symbol, side, price, quantity, locked_asset, locked_amount, fee_rebate):
        kwargs = {
            "price": price,
            "quantity": quantity,
            "time_in_force": OrderTimeInForceChoice.GTC,
        }
        order = cls.create_base_order(
            account_id=account_id,
            client_order_id=client_order_id,
            symbol=symbol,
            side=side,
            type=SpotOrderTypeChoice.LIMIT,
            locked_asset=locked_asset,
            locked_amount=locked_amount,
            fee_rebate=fee_rebate,
            **kwargs
        )
        return order