from utils.serializers import CustomModelSerializer
from ...models import Trade


class PerpTradeSerializer(CustomModelSerializer):
    class Meta:
        model = Trade
        fields = ['order', 'price', 'size', 'is_maker', 'contract', 'created_at']

