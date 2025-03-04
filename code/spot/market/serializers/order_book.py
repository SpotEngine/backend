from utils.serializers import ShortDecimalField, CustomModelSerializer
from ...models import Order
from rest_framework import serializers
from django.conf import settings


class OrderBookRowSerializer(serializers.Serializer):
    price = ShortDecimalField(max_digits=settings.BASE_MODEL_MAX_DIGITS, decimal_places=settings.BASE_MODEL_DECIMAL_PLACES)
    quantity = ShortDecimalField(max_digits=settings.BASE_MODEL_MAX_DIGITS, decimal_places=settings.BASE_MODEL_DECIMAL_PLACES)
    fee = ShortDecimalField(max_digits=settings.BASE_MODEL_MAX_DIGITS, decimal_places=settings.BASE_MODEL_DECIMAL_PLACES, default='0.0')


class OrderBookSerializer(serializers.Serializer):
    timestamp = serializers.IntegerField()
    symbol = serializers.CharField(max_length=15)
    asks = OrderBookRowSerializer(many=True)
    bids = OrderBookRowSerializer(many=True)


