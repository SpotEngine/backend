from utils.serializers import CustomModelSerializer
from ...models import Contract


class PerpTraderContractSerializer(CustomModelSerializer):
    class Meta:
        model = Contract
        fields = ['base', 'quote', 'lot_size', 'tick_size', 'max_size']

    def create(self, validated_data):
        obj = Contract.create(
            base=validated_data['base'],
            quote=validated_data['quote'],
            lot_size=validated_data['lot_size'],
            tick_size=validated_data['tick_size'],
            max_size=validated_data['max_size'],
        )
        return obj