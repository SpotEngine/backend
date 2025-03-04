from utils.serializers import CustomModelSerializer
from ...models import Position


class PerpPositionSerializer(CustomModelSerializer):
    class Meta:
        model = Position
        fields = [
            'status', 'contract', 'size', 'entry_price', 'direction', 'leverage', 
            'liquidation_price', 'margin', 'mode', 'margin_amount',
            'hard_liquidation_price'
        ]

