from utils.serializers import CustomModelSerializer
from ...models import Trade


class TradeMarketSerializer(CustomModelSerializer):
    class Meta:
        model = Trade
        fields = ['price', 'quantity', 'is_maker', 'symbol', 'created_at']
