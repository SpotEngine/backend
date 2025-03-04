from decimal import Decimal
from utils.choices import OrderStatusChoice, PerpDirectionChoice,PerpOrderTypeChoice
from utils.enums import ZERO
from ..models import Order, Trade, Position, PerpetualWallet
from django.db.transaction import atomic, on_commit
from .trade import create_trade
from .cancel import cancel_order
from .event import publish_new_events
from .liquidation import force_fill
from uuid import uuid4
from django.conf import settings



@atomic
def receive_send_order_event(event):
    order = Order.objects.select_for_update().filter(pk=event['id']).first()
    if not order.status == OrderStatusChoice.RECEIVED:
        return False
    match_tag = str(uuid4())
    updated_objects = match_order(
        order=order,
        updated_objects=set([order]),
        match_tag=match_tag,
    )
    on_commit(lambda: publish_new_events(updated_objects=updated_objects, trigger=order))
    


def match_order(order: Order, updated_objects: set, match_tag: str, offset: int = 0) -> dict:
    if order.direction == PerpDirectionChoice.LONG:
        opposite_direction = PerpDirectionChoice.SHORT
        price_order_by = 'price'
    else:
        opposite_direction = PerpDirectionChoice.LONG
        price_order_by = '-price'
    maker_orders_query = {
        'status': OrderStatusChoice.PLACED,
        'contract': order.contract,
        'direction': opposite_direction,
    }
    if order.type ==PerpOrderTypeChoice.LIMIT:
        if order.direction == PerpDirectionChoice.LONG:
            maker_orders_query['price__lte'] = order.price
        else:
            maker_orders_query['price__gte'] = order.price

    limit = settings.PERPETUAL_MATCH_ENGINE_ORDER_SELECT_SIZE
    maker_orders = Order.objects.select_for_update().filter(
        **maker_orders_query
    ).order_by(
        price_order_by,
        '-created_at',
    )[offset:offset+limit]
    if maker_orders.count() > 0:
        for maker_order in maker_orders:
            if maker_order.account_id == order.account_id:
                continue
            _updated_objects = create_trade(
                taker=order,
                maker=maker_order,
                match_tag=match_tag,
            )
            if _updated_objects is None:
                break
            updated_objects = updated_objects.union(_updated_objects)
            if order.status == OrderStatusChoice.FILLED:
                return updated_objects
        return match_order(order=order, updated_objects=updated_objects, match_tag=match_tag, offset=offset+limit)
    if order.status == OrderStatusChoice.RECEIVED:
        if order.type ==PerpOrderTypeChoice.LIMIT:
            if order.liquidation:
                _updated_objects = force_fill(order, opposite_direction)
                updated_objects = updated_objects.union(_updated_objects)
            else:
                order.status = OrderStatusChoice.PLACED
        else:
            updated_objects = cancel_order(order=order, updated_objects=updated_objects)
    order.save()
    return updated_objects

