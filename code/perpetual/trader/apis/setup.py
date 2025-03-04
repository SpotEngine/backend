from utils.model_viewsets import AccountCustomModelViewset
from ..serializers import PerpSetupSerializer
from ...models import Setup, Contract
from rest_framework.generics import get_object_or_404

class SetupViewSet(
    AccountCustomModelViewset, 
    ):
    http_method_names = [
        "get",
        "patch",
        "head",
        "options",
        "trace",
    ]
    serializer_class = PerpSetupSerializer
    lookup_field = 'symbol'
    

    def get_object(self):
        contract = get_object_or_404(Contract, symbol=self.kwargs['symbol'])
        obj = Setup.get_account_setup(account_id=self.account_id, contract=contract)
        return obj
