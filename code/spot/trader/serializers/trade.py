from utils.serializers import CustomModelSerializer
from ...models import Trade


class TradeSerializer(CustomModelSerializer):
    class Meta:
        model = Trade
        fields = ['order', 'price', 'quantity', 'is_maker', 'symbol', 'ctime', 'side', 'received_fee', 'received_amount', 'paid_rebate', 'paid_amount', 'received_token', 'paid_token']

