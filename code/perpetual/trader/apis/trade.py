from utils.model_viewsets import AccountModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from ..serializers import PerpTradeSerializer
from ...models import Trade


class TradeViewSet(
    AccountModelViewSet, 
    ListModelMixin, 
    RetrieveModelMixin, 
    ):
    serializer_class = PerpTradeSerializer


    def get_queryset_filter_kwargs(self):
        return {'order__account_id': self.account_id}
