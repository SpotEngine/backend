from rest_framework import serializers
from utils.serializers import CustomModelSerializer
from ...models import Contract


class ContractSerializer(CustomModelSerializer):
    class Meta:
        model = Contract
        exclude = ['priority']
