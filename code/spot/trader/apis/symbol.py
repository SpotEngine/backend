from utils.model_viewsets import AccountCustomModelViewset
from rest_framework.mixins import CreateModelMixin
from ..serializers import SpotTraderSymbolSerializer
# from ...models import Contract


class SymbolViewSet(
    AccountCustomModelViewset, 
    ):
    http_method_names = [
        "get",
        "post",
        # # "put",
        # "patch",
        # "delete",
        "head",
        "options",
        "trace",
    ]
    serializer_class = SpotTraderSymbolSerializer
    search_fields = ['symbol',]


    # def get_queryset_filter_kwargs(self):
    #     return {'order__account_id': self.account_id}
