from utils.model_viewsets import AccountModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from utils.enums import KafkaPerpEvent
from ...models import Trade
from ..filters import OrderFilter
from ..serializers import PerpOrderSerializer, PerpLimitOrderSerializer, PerpTradeSerializer, PerpMarketReduceOrderSerializer, PerpMarketAddOrderSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.response import Response
from django.db.transaction import atomic, on_commit
from ...kafka.client import publish
from ...logics.match import publish_new_events
from rest_framework.serializers import ValidationError


class OrderViewSet(
    AccountModelViewSet, 
    ListModelMixin, 
    RetrieveModelMixin, 
    DestroyModelMixin
    ):
    serializer_class = PerpOrderSerializer
    filterset_class = OrderFilter
    search_fields = ['contract__symbol',]


    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        # if order.liquidation:
        #     raise ValidationError({"liquidation": "liquidation order can't be canceled"})
        publish(
            info={'id': order.id, 'contract': order.contract.symbol},
            event_type=KafkaPerpEvent.CANCEL_ORDER,
        )
        return Response(status=HTTP_204_NO_CONTENT)

    def _receive_order(self, request):
        account_id = self.account_id
        serializer = self.get_serializer(data=request.data, context={'request': request, 'account_id': account_id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save(account_id=account_id)
        order_serializer = PerpOrderSerializer(instance=order)
        data = order_serializer.data
        on_commit(lambda: (
            publish(
                info={'account_id': account_id, **data},
                event_type=KafkaPerpEvent.SEND_ORDER,
            ), 
            publish_new_events(
                set([order.locked.asset, order]),
                trigger=order
            )
        ))
        return Response(data=data, status=HTTP_201_CREATED)

    @swagger_auto_schema(method='POST', request_body=PerpLimitOrderSerializer, responses={HTTP_201_CREATED: PerpOrderSerializer})
    @action(methods=['POST'], detail=False, serializer_class=PerpLimitOrderSerializer)
    @atomic()
    def limit(self, request):
        return self._receive_order(request=request)

    @swagger_auto_schema(method='POST', request_body=PerpMarketReduceOrderSerializer, responses={HTTP_201_CREATED: PerpOrderSerializer})
    @action(methods=['POST'], detail=False, serializer_class=PerpMarketReduceOrderSerializer, url_path='market/reduce')
    @atomic()
    def market_reduce(self, request):
        return self._receive_order(request=request)

    @swagger_auto_schema(method='POST', request_body=PerpMarketAddOrderSerializer, responses={HTTP_201_CREATED: PerpOrderSerializer})
    @action(methods=['POST'], detail=False, serializer_class=PerpMarketAddOrderSerializer, url_path='market/add')
    @atomic()
    def market_add(self, request):
        return self._receive_order(request=request)

    @swagger_auto_schema(method='GET', responses={HTTP_200_OK: PerpTradeSerializer(many=True)})
    @action(methods=['GET'], detail=True,)
    def trades(self, request, pk):
        order = self.get_object()
        queryset = Trade.objects.filter(order=order)
        return Response(data=PerpTradeSerializer(queryset, many=True).data, status=HTTP_200_OK)
