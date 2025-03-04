from utils.serializers import CustomModelSerializer, make_fields, CustomAccountModelSerializer
from rest_framework import serializers
from utils.choices import PositionStatusChoice, PerpDirectionChoice
from ...models import Order, PerpetualWallet, Setup, Position, OrderLock
from decimal import Decimal
from django.conf import settings
from utils.enums import ZERO


class PerpOrderSerializer(CustomModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class BaseCreatePerpOrderSerializer(CustomAccountModelSerializer):
    default_reduce_only = False

    class Meta:
        abstract = True


    def validate_price(self, price):
        if not price > Decimal('0.0'):
            raise serializers.ValidationError("should be positive")
        return price

    def validate_size(self, size):
        if not size > Decimal('0.0'):
            raise serializers.ValidationError("should be positive")
        return size

    def validate_and_lock_balance(self, locked_token, lock_amount):
        account_id = self.account_id
        locked_asset = PerpetualWallet.validate_and_lock_balance(
            account_id=account_id, 
            token=locked_token, 
            amount=lock_amount, 
            exception=serializers.ValidationError
        )
        return locked_asset

    
    def validate_price_filter(self, contract, price):
        d = price / contract.tick_size
        if not int(d) == d:
            raise serializers.ValidationError({'price': 'invalid price: tick size'})
        
    def validate_size_filter(self, contract, size):
        d = size / contract.lot_size
        if not int(d) == d:
            raise serializers.ValidationError({'size': 'invalid size: lot size'})
        elif size > contract.max_size:
            raise serializers.ValidationError({'size': 'invalid size: max size'})

    def validate_filters(self, attrs):
        contract = attrs['contract']
        if 'price' in attrs:
            self.validate_price_filter(contract=contract, price=attrs['price'])
        if 'size' in attrs:
            self.validate_size_filter(contract=contract, size=attrs['size'])

    def validate(self, attrs):
        reduce_only = attrs.get('reduce_only', self.default_reduce_only)
        attrs['reduce_only'] = reduce_only
        attrs = super().validate(attrs)
        self.validate_filters(attrs)
        setup = Setup.get_account_setup(account_id=self.account_id, contract=attrs['contract'])
        order_lock = self.get_order_lock(attrs=attrs, leverage=setup.leverage)
        kwargs = {
            "locked": order_lock,
            "leverage": setup.leverage,
            "margin": setup.margin,
            "mode": setup.mode,
        }
        return {**attrs, **kwargs}
    
    def _get_locked_asset_balance(self, attrs):
        raise NotImplementedError

    def get_order_lock(self, attrs, leverage):
        account_id = self.account_id
        if attrs['reduce_only']:
            size = attrs['size']
            try:
                position = Position.objects.select_for_update().get(
                    account_id=account_id, 
                    contract=attrs['contract'],
                    status=PositionStatusChoice.OPEN,
                    direction=PerpDirectionChoice.LONG if attrs['direction'] == PerpDirectionChoice.SHORT else PerpDirectionChoice.SHORT
                    )
            except Position.DoesNotExist:
                raise serializers.ValidationError({'reduce_only': 'not enough position size to reduce'})
            if size > position.size - position.locked_size:             
                raise serializers.ValidationError({'reduce_only': 'not enough position size to reduce'})
            order_lock = OrderLock.create(account_id=account_id, position=position, size=size)
            # position.locked_size += size
            position.save()
        else:
            locked_token, locked_amount = self._get_locked_asset_balance(attrs=attrs)
            locked_fee = locked_amount * settings.PERPETUAL_TAKER_FEE
            locked_amount /= leverage
            locked_asset = PerpetualWallet.validate_and_lock_balance(
                account_id=account_id, 
                token=locked_token, 
                amount=locked_amount+locked_fee, 
                exception=serializers.ValidationError
            )
            order_lock = OrderLock.create(account_id=account_id, asset=locked_asset, amount=locked_amount, fee=locked_fee)

        return order_lock
    
    def _create(self, validated_data):
        raise ModuleNotFoundError
    
    def create(self, validated_data):
        order = self._create(validated_data)
        return order
    

class PerpMarketReduceOrderSerializer(BaseCreatePerpOrderSerializer):
    default_reduce_only = True

    class Meta:
        model = Order
        fields, extra_kwargs = make_fields(
            required_fields=[
                'client_order_id',
                'contract',
                'direction',
                'size',
            ],
        )
    
    
    def create(self, validated_data):
        order = Order.create_market_reduce_order(**validated_data)
        return order
    

class PerpMarketAddOrderSerializer(BaseCreatePerpOrderSerializer):
    class Meta:
        model = Order
        fields, extra_kwargs = make_fields(
            required_fields=[
                'client_order_id',
                'contract',
                'direction',
                'quote_quantity',
            ],
        )
    
    
    def _get_locked_asset_balance(self, attrs):
        contract = attrs['contract']
        locked_token = contract.quote
        locked_amount = attrs['quote_quantity']
        return locked_token, locked_amount

    def create(self, validated_data):
        order = Order.create_market_add_order(**validated_data)
        return order
    


class PerpLimitOrderSerializer(BaseCreatePerpOrderSerializer):

    class Meta:
        model = Order
        fields, extra_kwargs = make_fields(
            required_fields=[
                'client_order_id',
                'contract',
                'direction',
                'price',
                'size',
            ],
            optional_fields=[
                # 'post_only',
                'reduce_only',
            ]
        )
    
    def _get_locked_asset_balance(self, attrs):
        contract = attrs['contract']
        locked_token = contract.quote
        locked_amount = attrs['price'] * attrs['size']
        return locked_token, locked_amount
    
    def create(self, validated_data):
        order = Order.create_limit_order(**validated_data)
        return order
    
