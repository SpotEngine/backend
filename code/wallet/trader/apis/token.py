from utils.model_viewsets import AccountCustomModelViewset
from rest_framework.mixins import CreateModelMixin
from ..serializers import TokenSerializer
# from ...models import Contract


class TokenViewSet(
    AccountCustomModelViewset, 
    CreateModelMixin
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
    serializer_class = TokenSerializer
    search_fields = ['ticker', 'name']

    

    # def get_queryset_filter_kwargs(self):
    #     return {'order__account_id': self.account_id}
