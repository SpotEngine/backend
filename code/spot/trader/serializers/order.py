from utils.serializers import CustomModelSerializer, make_fields, CustomAccountModelSerializer
from rest_framework import serializers
from ...models import Order
from wallet.models import Asset
from utils.choices import SpotOrderSideChoice
from decimal import Decimal


class SpotOrderSerializer(CustomModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class BaseCreateSpotOrderSerializer(CustomAccountModelSerializer):
    class Meta:
        abstract = True
    

    def validate_price(self, price):
        if not price > Decimal('0.0'):
            raise serializers.ValidationError("should be positive")
        return price

    def validate_quantity(self, quantity):
        if not quantity > Decimal('0.0'):
            raise serializers.ValidationError("should be positive")
        return quantity

    def validate_fee_rebate(self, fee_rebate):
        if not -1 < fee_rebate < 1:
            raise serializers.ValidationError("wrong value")
        return fee_rebate

    def validate_and_lock_balance(self, locked_token, lock_amount):
        account_id = self.account_id
        lock_asset = Asset.validate_and_lock_balance(
            account_id=account_id, 
            token=locked_token, 
            amount=lock_amount, 
            exception=serializers.ValidationError
        )
        return lock_asset
    
    def _get_locked_asset_balance(self, attrs):
        raise NotImplementedError

    def get_locked_asset_balance(self, attrs):
        locked_token, locked_amount = self._get_locked_asset_balance(attrs=attrs)
        return locked_token, locked_amount.normalize()
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        locked_token, locked_amount = self.get_locked_asset_balance(attrs=attrs)
        locked_asset = self.validate_and_lock_balance(locked_token=locked_token, lock_amount=locked_amount)
        kwargs = {
            "locked_asset": locked_asset,
            "locked_amount": locked_amount,
        }
        return {**attrs, **kwargs}

    def save(self, **kwargs):
        order = super().save(**kwargs)
        return order
    
class SpotLimitOrderSerializer(BaseCreateSpotOrderSerializer):

    class Meta:
        model = Order
        fields, extra_kwargs = make_fields(
            required_fields=[
                'client_order_id',
                'symbol',
                'side',
                'price',
                'quantity',
                'fee_rebate',
            ],
            optional_fields=[
                'post_only'
            ]
        )

    
    def _get_locked_asset_balance(self, attrs):
        symbol = attrs['symbol']
        side = attrs['side']
        if side == SpotOrderSideChoice.BUY:
            locked_token = symbol.quote
            locked_amount = attrs['price'] * attrs['quantity']
        elif side == SpotOrderSideChoice.SELL:
            locked_token = symbol.base
            locked_amount = attrs['quantity']
        else:
            raise serializers.ValidationError(f"Invalid side {side}")
        return locked_token, locked_amount
    
    def create(self, validated_data):
        order = Order.create_limit_order(**validated_data)
        return order
    
class SpotMarketBuyOrderSerializer(BaseCreateSpotOrderSerializer):

    class Meta:
        model = Order
        fields, extra_kwargs = make_fields(
            required_fields=[
                'client_order_id',
                'symbol',
                'quote_quantity',
                'fee_rebate',
            ],
        )

    
    def _get_locked_asset_balance(self, attrs):
        symbol = attrs['symbol']
        locked_token = symbol.quote
        locked_amount = attrs['quote_quantity']
        return locked_token, locked_amount
    
    def create(self, validated_data):
        order = Order.create_market_buy_order(**validated_data)
        return order

class SpotMarketSellOrderSerializer(BaseCreateSpotOrderSerializer):

    class Meta:
        model = Order
        fields, extra_kwargs = make_fields(
            required_fields=[
                'client_order_id',
                'symbol',
                'quantity',
                'fee_rebate',
            ],
        )

    
    def _get_locked_asset_balance(self, attrs):
        symbol = attrs['symbol']
        locked_token = symbol.base
        locked_amount = attrs['quantity']
        return locked_token, locked_amount
    
    def create(self, validated_data):
        order = Order.create_market_sell_order(**validated_data)
        return order
    
      