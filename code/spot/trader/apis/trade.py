from utils.model_viewsets import AccountCustomModelViewset
from ..serializers import TradeSerializer
from ...models import Trade

class TradeViewSet(
    AccountCustomModelViewset, 
    ):
    http_method_names = [
        "get",
        "head",
        "options",
        "trace",
    ]
    serializer_class = TradeSerializer


    def get_queryset_filter_kwargs(self):
        return {'order__account_id': self.account_id}
