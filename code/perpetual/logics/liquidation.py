from utils.choices import OrderStatusChoice, PerpOrderTypeChoice, PositionStatusChoice, PerpDirectionChoice, OrderStatusChoice
from ..models import Order, Income, Trade, Position, PerpetualWallet, OrderLock

from django.db.transaction import atomic
from utils.enums import ZERO
from utils.helper import DecimalRound
from django.conf import settings


def force_fill(order: Order, opposite_direction):
    return set()
    # limit = settings.PERPETUAL_MATCH_ENGINE_ORDER_SELECT_SIZE
    # remained_size = order.size - order.filled_size
    # order_by = 'entry_price' if opposite_direction == PerpDirectionChoice.LONG else '-entry_price'
    # open_positions = Position.objects.filter(status=PositionStatusChoice.OPEN, contract=order.contract, direction=opposite_direction).order_by(order_by)[:limit]
    # closing_positions = []
    # for position in open_positions:
    #     pass
    #     order_locks = position.orderlock_set().filter(size__gt=ZERO)
    #     for order_lock in order_locks:
    #         orders = order_lock.order_set().filter(status__in=[OrderStatusChoice.PLACED, OrderStatusChoice.RECEIVED])
    #         for order in orders:
    #             cancel_order(order)
        
    #     # TODO: close open positions
    # pass

