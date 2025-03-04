# from django.db import models
# from utils.base_models import BaseModel, base_decimal
# from utils.choices import OrderStatusChoice, PerpDirectionChoice,PerpOrderTypeChoice, OrderTimeInForceChoice, MarginModeChoice, PositionModeChoice


# class Order(BaseModel):
#     account = models.ForeignKey("aaa.Account", on_delete=models.PROTECT, null=True, blank=True, related_name='perpetual_order')
#     contract = models.ForeignKey("Contract", on_delete=models.PROTECT, null=True, blank=True)
#     client_order_id = models.CharField(unique=True, max_length=40,)
    
#     status = models.CharField(default=OrderStatusChoice.RECEIVED, max_length=15, choices=OrderStatusChoice.choices, null=True, blank=True)
#     direction = models.CharField(default=PerpDirectionChoice.LONG, max_length=5, choices=PerpDirectionChoice.choices, null=True, blank=True)
#     type = models.CharField(default=PerpOrderTypeChoice.LIMIT, max_length=20, choices=PerpOrderTypeChoice.choices, null=True, blank=True)
#     leverage = models.IntegerField(default=10, null=True, blank=True)    
#     margin = models.CharField(default=MarginModeChoice.ISOLATED, max_length=20, choices=MarginModeChoice.choices, null=True, blank=True)
#     mode = models.CharField(default=PositionModeChoice.ONEWAY, max_length=20, choices=PositionModeChoice.choices, null=True, blank=True)
#     time_in_force = models.CharField(default=OrderTimeInForceChoice.GTC, max_length=5, choices=OrderTimeInForceChoice.choices, null=True, blank=True)
#     post_only = models.BooleanField(default=False, null=True, blank=True)
    
#     price = base_decimal()
#     size = base_decimal()
#     filled_size = base_decimal()

#     quote_quantity = base_decimal()
#     filled_quote_quantity = base_decimal()

#     locked_asset = models.ForeignKey("PerpetualWallet", on_delete=models.PROTECT, null=True, blank=True)
#     locked_amount = base_decimal()
#     locked_fee = base_decimal()
#     post_only = models.BooleanField(default=False, null=True, blank=True)
#     reduce_only = models.BooleanField(default=False, null=True, blank=True)


#     class Meta:
#         indexes = [
#             models.Index(fields=['direction', 'price',]),
#         ]
#     def __str__(self):
#         return f'{self.direction}:{self.id}'
#     @classmethod
#     def create_base_order(cls, account_id, client_order_id, contract, locked_asset, locked_amount, direction, type, **kwargs):
#         order = cls.objects.create(
#             account_id=account_id,
#             client_order_id=client_order_id,
#             contract=contract,
#             direction=direction,
#             type=type,            
#             locked_asset=locked_asset,
#             locked_amount=locked_amount,
#             **kwargs
#         )
#         return order

#     @classmethod
#     def create_limit_order(cls, account_id, client_order_id, contract, direction, price, size, locked_asset, locked_amount, **kwargs):
#         kwargs["price"] = price
#         kwargs["size"] = size
#         kwargs["time_in_force"] = OrderTimeInForceChoice.GTC
#         order = cls.create_base_order(
#             account_id=account_id,
#             client_order_id=client_order_id,
#             contract=contract,
#             direction=direction,
#             type=PerpOrderTypeChoice.LIMIT,
#             locked_asset=locked_asset,
#             locked_amount=locked_amount,
#             **kwargs
#         )
#         return order