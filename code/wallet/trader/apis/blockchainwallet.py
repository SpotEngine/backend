from utils.model_viewsets import UserModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from ..serializers import BlockchainWalletSerializer


class BlockchainWalletViewSet(UserModelViewSet, CreateModelMixin, ListModelMixin):
    http_method_names = [
        "get",
        "post",
        "head",
        "options",
        "trace",
    ]
    serializer_class = BlockchainWalletSerializer


