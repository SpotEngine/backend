from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.response import Response
from django.db.models import F, Sum
from rest_framework.decorators import action
from utils.model_viewsets import NoAuthReadOnlyModelViewSet
from ..serializers import SymbolSerializer, OrderBookSerializer
from utils.enums import ZERO
from utils.choices import OrderStatusChoice, SpotOrderSideChoice
import time


class SymbolViewSet(
    NoAuthReadOnlyModelViewSet, 
    ):
    serializer_class = SymbolSerializer
    select_related_fields = ['base', 'quote']
    search_fields = ['symbol', ]

    @action(methods=['get'], detail=True)
    def orderbook(self, request, pk):
        symbol = self.get_object()
        open_orders = symbol.order_set.filter(status=OrderStatusChoice.PLACED).annotate(net_quantity=F('quantity')-F('filled_quantity'))
        bids = self._sort_orderbook_rows(orders_qs=open_orders, side=SpotOrderSideChoice.BUY)
        asks = self._sort_orderbook_rows(orders_qs=open_orders, side=SpotOrderSideChoice.SELL)
        serializer = OrderBookSerializer(instance={
            'symbol': pk,
            'timestamp': int(time.time()*1000),
            'asks': asks,
            'bids': bids,
        })
        return Response(serializer.data, status=HTTP_200_OK)
    
    def _sort_orderbook_rows(self, orders_qs, side):
        order_by_price = '-price' if side == SpotOrderSideChoice.BUY else 'price'
        orders = orders_qs.filter(side=side).order_by(order_by_price, '-fee_rebate', '-created_at')[:100]
        rows = []
        price = ZERO
        for order in orders:
            if any([not price == order.price, rows and not rows[-1]['fee'] == order.fee_rebate]):
                rows.append({
                    'price': order.price,
                    'fee': order.fee_rebate,
                    'quantity': order.net_quantity,
                })
                price = order.price
            elif rows[-1]['fee'] == order.fee_rebate:
                rows[-1]['quantity'] += order.net_quantity
        return rows