from utils.serializers import CustomModelSerializer
from rest_framework import serializers
from ...models import Setup


class PerpSetupSerializer(CustomModelSerializer):
    leverage = serializers.ChoiceField(choices=[1,2,5,10,20,50,100], required=False)
    class Meta:
        model = Setup
        fields = ['contract', 'margin', 'mode', 'leverage']
        extra_kwargs = {
            'contract': {'read_only': True},
            # 'leverage': {'min_value': 1},
        }

    def validate_leverage(self, leverage):
        leverage = int(leverage)
        setup = self.instance
        if leverage > setup.contract.max_leverage:
            raise serializers.ValidationError(f'max leverage is {setup.contract.max_leverage}')
        return leverage