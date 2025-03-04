from utils.model_viewsets import AccountModelViewSet
from rest_framework.mixins import CreateModelMixin
from ..serializers import PerpTraderContractSerializer
# from ...models import Contract


class ContractViewSet(
    AccountModelViewSet, 
    CreateModelMixin
    ):
    serializer_class = PerpTraderContractSerializer


    # def get_queryset_filter_kwargs(self):
    #     return {'order__account_id': self.account_id}
