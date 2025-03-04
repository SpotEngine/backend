from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK
from utils.model_viewsets import NoAuthReadOnlyModelViewSet
from utils.choices import OrderStatusChoice, PerpDirectionChoice
from ..serializers import ContractSerializer, PerpOrderBookSerializer
from rest_framework.response import Response
from django.db.models import F, Sum
from collections import defaultdict
from utils.enums import ZERO
import time


class ContractViewSet(
    NoAuthReadOnlyModelViewSet, 
    ):
    serializer_class = ContractSerializer
    select_related_fields = ['quote',]
    search_fields = ['symbol',]
    
    @action(methods=['get'], detail=True)
    def orderbook(self, request, pk):
        contract = self.get_object()
        open_orders = contract.order_set.filter(status=OrderStatusChoice.PLACED).annotate(net_size=F('size')-F('filled_size'))

        asks_prices = defaultdict(lambda: ZERO)
        for ask in open_orders.filter(direction=PerpDirectionChoice.SHORT).order_by('price')[:100]:
            asks_prices[ask.price] += ask.net_size

        bids_prices = defaultdict(lambda: ZERO)
        for bid in open_orders.filter(direction=PerpDirectionChoice.LONG).order_by('-price')[:100]:
            bids_prices[bid.price] += bid.net_size
        serializer = PerpOrderBookSerializer(instance={
            'contract': pk,
            'timestamp': int(time.time()*1000),
            'asks': [{'price': price, 'size': asks_prices[price]} for price in sorted(asks_prices)],
            'bids': [{'price': price, 'size': bids_prices[price]} for price in sorted(bids_prices, reverse=True)],
        })
        return Response(serializer.data, status=HTTP_200_OK)