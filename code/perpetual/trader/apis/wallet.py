from utils.model_viewsets import AccountModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from ...models import PerpetualWallet
from ..serializers import PerpWalletSerializer
from ..filters import PerpWalletFilter

class PerpWalletViewSet(
    AccountModelViewSet, 
    ListModelMixin, 
    RetrieveModelMixin, 
    ):
    serializer_class = PerpWalletSerializer
    filterset_class = PerpWalletFilter

    def get_queryset(self):
        return PerpetualWallet.objects.filter(account_id=self.account_id)
