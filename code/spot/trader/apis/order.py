from utils.model_viewsets import AccountModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from ..serializers import SpotOrderSerializer, SpotLimitOrderSerializer, SpotMarketSellOrderSerializer, SpotMarketBuyOrderSerializer, TradeSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.response import Response
from django.db.transaction import atomic, on_commit
from ...kafka.client import publish
from utils.enums import KafkaSpotEvent
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from ..filters import OrderFilter
from ...logics.match import publish_new_events
from ...models import Trade


class OrderViewSet(
    AccountModelViewSet, 
    ListModelMixin, 
    RetrieveModelMixin, 
    DestroyModelMixin
    ):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OrderFilter
    serializer_class = SpotOrderSerializer

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        publish(
            info={'id': order.id, 'symbol': order.symbol.symbol},
            event_type=KafkaSpotEvent.CANCEL_ORDER,
        )
        return Response(status=HTTP_204_NO_CONTENT)

    def _receive_order(self, request):
        account_id = self.account_id
        serializer = self.get_serializer(data=request.data, context={'request': request, 'account_id': account_id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save(account_id=account_id)
        order_serializer = SpotOrderSerializer(instance=order)
        data = order_serializer.data
        on_commit(lambda: (
            publish(
                info={'account_id': account_id, **data},
                event_type=KafkaSpotEvent.SEND_ORDER,
            ), 
            publish_new_events(
                set([order.locked_asset, order]),
                trigger=order
            )
        ))
        return Response(data=data, status=HTTP_201_CREATED)

    @swagger_auto_schema(method='POST', request_body=SpotLimitOrderSerializer, responses={HTTP_201_CREATED: SpotOrderSerializer})
    @action(methods=['POST'], detail=False, serializer_class=SpotLimitOrderSerializer)
    @atomic()
    def limit(self, request):
        return self._receive_order(request=request)

    @swagger_auto_schema(method='POST', request_body=SpotMarketBuyOrderSerializer, responses={HTTP_201_CREATED: SpotOrderSerializer})
    @action(methods=['POST'], detail=False, serializer_class=SpotMarketBuyOrderSerializer, url_path='market/buy')
    @atomic()
    def market_buy(self, request):
        return self._receive_order(request=request)

    @swagger_auto_schema(method='POST', request_body=SpotMarketSellOrderSerializer, responses={HTTP_201_CREATED: SpotOrderSerializer})
    @action(methods=['POST'], detail=False, serializer_class=SpotMarketSellOrderSerializer, url_path='market/sell')
    @atomic()
    def market_sell(self, request):
        return self._receive_order(request=request)


    @swagger_auto_schema(method='GET', responses={HTTP_200_OK: TradeSerializer(many=True)})
    @action(methods=['GET'], detail=True,)
    def trades(self, request, pk):
        order = self.get_object()
        queryset = Trade.objects.filter(order=order)
        return Response(data=TradeSerializer(queryset, many=True).data, status=HTTP_200_OK)
