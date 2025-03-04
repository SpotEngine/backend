from utils.model_viewsets import AccountCustomModelViewset
from ..serializers import AssetSerializer
from rest_framework.decorators import action
from ..filters import AssetFilter


class AssetViewSet(AccountCustomModelViewset):
    http_method_names = [
        "get",
        "head",
        "options",
        "trace",
    ]
    serializer_class = AssetSerializer
    filterset_class = AssetFilter



