from utils.serializers import ShortDecimalField, CustomModelSerializer
from ...models import Order
from rest_framework import serializers
from django.conf import settings



class PerpOrderBookRowSerializer(serializers.Serializer):
    price = ShortDecimalField(max_digits=settings.BASE_MODEL_MAX_DIGITS, decimal_places=settings.BASE_MODEL_DECIMAL_PLACES)
    size = ShortDecimalField(max_digits=settings.BASE_MODEL_MAX_DIGITS, decimal_places=settings.BASE_MODEL_DECIMAL_PLACES)


class PerpOrderBookSerializer(serializers.Serializer):
    timestamp = serializers.IntegerField()
    contract = serializers.CharField(max_length=15)
    asks = PerpOrderBookRowSerializer(many=True)
    bids = PerpOrderBookRowSerializer(many=True)


