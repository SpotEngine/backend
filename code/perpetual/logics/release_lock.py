from utils.choices import OrderStatusChoice, PerpOrderTypeChoice, PositionStatusChoice, PerpDirectionChoice
from ..models import Order, Income, Trade, Position, PerpetualWallet, OrderLock
from django.db.transaction import atomic
from utils.enums import ZERO
from utils.helper import DecimalRound
from django.conf import settings


def release(locked: OrderLock):
    update = None
    if locked.amount + locked.fee > ZERO:
        update = PerpetualWallet.add_to_asset(
            account=locked.account, 
            token=locked.asset.token, 
            quantity=locked.amount+locked.fee
        )
        locked.amount = ZERO
        locked.fee = ZERO
    elif locked.size > ZERO:
        # locked.position.locked_size -= locked.size
        locked.size = ZERO
    locked.save()
    return update

