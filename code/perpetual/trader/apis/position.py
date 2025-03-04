from utils.model_viewsets import AccountModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
from ...models import Position
from utils.choices import PositionStatusChoice
from ..serializers import PerpPositionSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.response import Response
from django.db.transaction import atomic, on_commit
from ...kafka.client import publish


class PositionViewSet(
    AccountModelViewSet, 
    ListModelMixin, 
    RetrieveModelMixin, 
    ):
    serializer_class = PerpPositionSerializer

    def get_queryset(self):
        return Position.objects.filter(account_id=self.account_id, status=PositionStatusChoice.OPEN)

    # @action(methods=['post'], detail=True,)
    # def close(self, request, pk):
    #     position = self.get_object()
    #     position.close()
    #     return Response({},)