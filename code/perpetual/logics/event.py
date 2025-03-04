from decimal import Decimal
from ..kafka.client import publish
from utils.choices import OrderStatusChoice, PerpDirectionChoice,PerpOrderTypeChoice
from utils.enums import ZERO, SystemGeneratedEvent, KafkaPerpEvent
from utils.helper import SystemEvent
from ..models import Order, Trade, Position, PerpetualWallet
from ..trader.serializers import PerpOrderSerializer, PerpTradeSerializer, PerpPositionSerializer
from ..market.serializers import PerpTradeMarketSerializer, PerpOrderBookSerializer
from wallet.trader.serializers import AssetSerializer
from connection.broadcast import Broadcast
from collections import defaultdict
from django.conf import settings



def publish_new_events(updated_objects: set, trigger):
    updates = []
    order_book_updates = {'timestamp': 0, 'bids': defaultdict(lambda: ZERO), 'asks': defaultdict(lambda: ZERO)}
    if trigger:
        order_book_updates["contract"] = trigger.contract.symbol

    if isinstance(trigger, Order):
        order_book_updates['timestamp'] = trigger.utime
        if trigger.status == OrderStatusChoice.CANCELED:
            order_book_side = 'bids' if trigger.direction == PerpDirectionChoice.LONG else 'asks'
            order_book_updates[order_book_side][trigger.price] -= trigger.size - trigger.filled_size 
        elif trigger.status == OrderStatusChoice.PLACED:
            order_book_side = 'bids' if trigger.direction == PerpDirectionChoice.LONG else 'asks'
            order_book_updates[order_book_side][trigger.price] += trigger.size - trigger.filled_size 
        

    for obj in updated_objects:
        if isinstance(obj, SystemEvent):
            if obj.event == SystemGeneratedEvent.LIQUIDATION_ORDER:
                publish(
                    info=obj.data,
                    event_type=KafkaPerpEvent.SEND_ORDER,
                )
        if isinstance(obj, Order):
            updates.append({
                "channel": f"account_{obj.account.id}",
                "message": {
                    "event": "PERP_ACCOUNT_ORDER",
                    "data": PerpOrderSerializer(obj).data,
                }
            })

        elif isinstance(obj, Trade):
            account_trade_data = PerpTradeSerializer(obj).data
            updates.append({
                "channel": f"account_{obj.order.account.id}",
                "message": {
                    "event": "PERP_ACCOUNT_TRADE",
                    "data": account_trade_data,
                }
            })
            if obj.is_maker:
                market_trade_data = PerpTradeMarketSerializer(obj).data
                updates.append({
                    "channel": f"trade_{obj.contract.symbol}",
                    "message": {
                        "event": "PERP_MARKET_TRADE",
                        "data": market_trade_data,
                    }
                })
                updates.append({
                    "channel": f"trade_all",
                    "message": {
                        "event": "PERP_MARKET_TRADE",
                        "data": market_trade_data,
                    }
                })
                order_book_side = 'bids' if obj.order.direction == PerpDirectionChoice.LONG else 'asks'
                order_book_updates[order_book_side][obj.price] -= obj.size 
        elif isinstance(obj, PerpetualWallet):
            updates.append({
                "channel": f"account_{obj.account.id}",
                "message": {
                    "event": "PERP_ACCOUNT_BALANCE",
                    "data": AssetSerializer(obj).data,
                }
            })
        elif isinstance(obj, Position):
            updates.append({
                "channel": f"account_{obj.account.id}",
                "message": {
                    "event": "PERP_ACCOUNT_POSITION",
                    "data": PerpPositionSerializer(obj).data,
                }
            })

    if order_book_updates["bids"] or order_book_updates["asks"]:  
        order_book_updates["bids"] = [{'price': price, 'size': size} for price, size in order_book_updates["bids"].items()]
        order_book_updates["asks"] = [{'price': price, 'size': size} for price, size in order_book_updates["asks"].items()]
        order_book_data = PerpOrderBookSerializer(instance=order_book_updates).data
        updates.append({
            "channel": f"orderbook_{order_book_updates['contract']}",
            "message": {
                "event": "PERP_MARKET_ORDERBOOK",
                "data": order_book_data,
            }
        })
        updates.append({
            "channel": f"orderbook_all",
            "message": {
                "event": "PERP_MARKET_ORDERBOOK",
                "data": order_book_data,
            }
        })
    Broadcast.batch_publish(updates=updates)