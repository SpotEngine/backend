from decimal import Decimal
import json
from utils.choices import OrderStatusChoice, SpotOrderSideChoice, SpotOrderTypeChoice
from utils.enums import ZERO
from ..models import Order, Trade
from wallet.models import Asset
from django.db.transaction import atomic, on_commit
from .trade import create_trade
from ..trader.serializers import SpotOrderSerializer, TradeSerializer
from ..market.serializers import TradeMarketSerializer, OrderBookSerializer
from wallet.trader.serializers import AssetSerializer
from connection.broadcast import Broadcast
from collections import defaultdict
from django.conf import settings
from uuid import uuid4


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
    

def cancel_order(order: Order, updated_objects: set) -> dict:
    order.status = OrderStatusChoice.CANCELED
    if order.locked_amount > Decimal('0.0'):
        updated_asset = Asset.add_to_asset(account=order.account, token=order.locked_asset.token, quantity=order.locked_amount)
        order.locked_amount = Decimal('0.0')
    order.save()
    updated_objects.add(updated_asset)
    return updated_objects


def match_order(order: Order, updated_objects: set, match_tag: str, offset: int = 0) -> dict:
    if order.side == SpotOrderSideChoice.BUY:
        opposite_side = SpotOrderSideChoice.SELL
        price_order_by = 'price'
    else:
        opposite_side = SpotOrderSideChoice.BUY
        price_order_by = '-price'
    maker_orders_query = {
        'status': OrderStatusChoice.PLACED,
        'symbol': order.symbol,
        'side': opposite_side,
        'fee_rebate__gte': -order.fee_rebate,
    }

    if order.type == SpotOrderTypeChoice.LIMIT:
        if order.side == SpotOrderSideChoice.BUY:
            maker_orders_query['price__lte'] = order.price
        else:
            maker_orders_query['price__gte'] = order.price

    limit = settings.SPOT_MATCH_ENGINE_ORDER_SELECT_SIZE
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
        if order.type == SpotOrderTypeChoice.LIMIT:
            order.status = OrderStatusChoice.PLACED
        else:
            updated_objects = updated_objects.union(
                cancel_order(order=order, updated_objects=updated_objects)
            )
    order.save()
    return updated_objects


def publish_new_events(updated_objects: set, trigger):
    updates = []
    order_book_updates = {'timestamp': 0, 'bids': defaultdict(lambda: ZERO), 'asks': defaultdict(lambda: ZERO)}
    if trigger:
        order_book_updates["symbol"] = trigger.symbol.symbol

    if isinstance(trigger, Order):
        order_book_updates['timestamp'] = trigger.utime
        if trigger.status == OrderStatusChoice.CANCELED:
            order_book_side = 'bids' if trigger.side == SpotOrderSideChoice.BUY else 'asks'
            order_book_updates[order_book_side][trigger.price] -= trigger.quantity - trigger.filled_quantity 
        elif trigger.status == OrderStatusChoice.PLACED:
            order_book_side = 'bids' if trigger.side == SpotOrderSideChoice.BUY else 'asks'
            order_book_updates[order_book_side][trigger.price] += trigger.quantity - trigger.filled_quantity 

    for obj in updated_objects:
        if isinstance(obj, Order):
            updates.append({
                "channel": f"account_{obj.account.id}",
                "message": {
                    "event": "ACCOUNT_ORDER_UPDATE",
                    "data": SpotOrderSerializer(obj).data,
                }
            })
        elif isinstance(obj, Trade):
            account_trade_data = TradeSerializer(obj).data
            updates.append({
                "channel": f"account_{obj.order.account.id}",
                "message": {
                    "event": "ACCOUNT_TRADE_UPDATE",
                    "data": account_trade_data,
                }
            })
            if obj.is_maker:
                market_trade_data = TradeMarketSerializer(obj).data
                updates.append({
                    "channel": f"trade_{obj.symbol.symbol}",
                    "message": {
                        "event": "MARKET_TRADE_UPDATE",
                        "data": market_trade_data,
                    }
                })
                updates.append({
                    "channel": f"trade_all",
                    "message": {
                        "event": "MARKET_TRADE_UPDATE",
                        "data": market_trade_data,
                    }
                })
                order_book_side = 'bids' if obj.order.side == SpotOrderSideChoice.BUY else 'asks'
                order_book_updates[order_book_side][obj.price] -= obj.quantity 
        elif isinstance(obj, Asset):
            updates.append({
                "channel": f"account_{obj.account.id}",
                "message": {
                    "event": "ACCOUNT_BALANCE_UPDATE",
                    "data": AssetSerializer(obj).data,
                }
            })

    if order_book_updates["bids"] or order_book_updates["asks"]:  
        order_book_updates["bids"] = [{'price': price, 'quantity': quantity} for price, quantity in order_book_updates["bids"].items()]
        order_book_updates["asks"] = [{'price': price, 'quantity': quantity} for price, quantity in order_book_updates["asks"].items()]
        order_book_data = OrderBookSerializer(instance=order_book_updates).data
        updates.append({
            "channel": f"orderbook_{order_book_updates['symbol']}",
            "message": {
                "event": "MARKET_ORDERBOOK_UPDATE",
                "data": order_book_data,
            }
        })
        updates.append({
            "channel": f"orderbook_all",
            "message": {
                "event": "MARKET_ORDERBOOK_UPDATE",
                "data": order_book_data,
            }
        })
    Broadcast.batch_publish(updates=updates)