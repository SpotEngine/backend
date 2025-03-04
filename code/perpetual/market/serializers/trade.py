from utils.serializers import CustomModelSerializer
from ...models import Trade


class PerpTradeMarketSerializer(CustomModelSerializer):
    class Meta:
        model = Trade
        fields = ['price', 'size', 'is_maker', 'contract', 'created_at']
