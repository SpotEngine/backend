from decimal import Decimal
from utils.choices import OrderStatusChoice, PerpDirectionChoice,PerpOrderTypeChoice
from utils.enums import ZERO
from ..models import Order, Trade, Position, PerpetualWallet
from django.db.transaction import atomic, on_commit
from .event import publish_new_events
from .release_lock import release


@atomic
def receive_cancel_order_event(event):
    order = Order.objects.select_for_update().filter(pk=event['id']).first()
    if order.status == OrderStatusChoice.RECEIVED:
        trigger = None
    elif order.status == OrderStatusChoice.PLACED:
        trigger = order
    else:
        return False
    updated_objects = cancel_order(order=order, updated_objects=set([order]))
    on_commit(lambda: publish_new_events(updated_objects=updated_objects, trigger=trigger))
    

def cancel_order(order: Order, updated_objects: set) -> dict:
    order.status = OrderStatusChoice.CANCELED
    updated_asset = release(order.locked)
    order.save()
    if updated_asset:
        updated_objects.add(updated_asset)
    return updated_objects



