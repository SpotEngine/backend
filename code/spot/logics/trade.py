from decimal import Decimal
from utils.choices import OrderStatusChoice, SpotOrderSideChoice, SpotOrderTypeChoice
from ..models import Order, Income, Trade
from wallet.models import Asset
from django.db.transaction import atomic
from decimal import Decimal
from utils.enums import ZERO
from django.conf import settings


def get_filling_quantity(maker, taker):
    maker_max_trade_quantity = maker.quantity - maker.filled_quantity
    if taker.type == SpotOrderTypeChoice.LIMIT:
        taker_max_trade_quantity = taker.quantity - taker.filled_quantity
    elif taker.type == SpotOrderTypeChoice.MARKET:
        if taker.side == SpotOrderSideChoice.SELL:
            taker_max_trade_quantity = taker.quantity - taker.filled_quantity
        else:
            taker_max_quote_quantity = taker.quote_quantity - taker.filled_quote_quantity
            taker_max_trade_quantity = ZERO
            for i in range(int(maker_max_trade_quantity/maker.symbol.lot_size) + 1):
                trade_quantity_candidate = maker_max_trade_quantity - i * maker.symbol.lot_size
                if taker_max_quote_quantity >= trade_quantity_candidate * maker.price:
                    taker_max_trade_quantity = trade_quantity_candidate
                    break
    else:
        raise Exception(f'invalid order type: {taker.type}')

    filling_quantity = max(min(taker_max_trade_quantity, maker_max_trade_quantity), ZERO)
    return filling_quantity

@atomic
def create_trade(taker: Order, maker: Order, match_tag: str):
    assert taker.fee_rebate + maker.fee_rebate >= ZERO
    filling_quantity = get_filling_quantity(maker=maker, taker=taker)
    if filling_quantity == ZERO:
        return None
    trade_kwargs = {
        'symbol': maker.symbol,
        'price': maker.price,
        'quantity': filling_quantity,
        'match_tag': match_tag,
    }
    taker_trade = Trade.create(order=taker, paid_token=taker.locked_asset.token, received_token=maker.locked_asset.token, is_maker=False, **trade_kwargs)
    maker_trade = Trade.create(order=maker, paid_token=maker.locked_asset.token, received_token=taker.locked_asset.token, is_maker=True, **trade_kwargs)

    quote_quantity = maker.price * filling_quantity
    update_objects = set([maker])
    for is_maker in [True, False]:
        if is_maker:
            is_other_side_maker = False
            order = maker
            other_side_order = taker
            trade = maker_trade
            other_side_trade = taker_trade
        else:
            is_other_side_maker = True
            order = taker
            other_side_order = maker
            trade = taker_trade
            other_side_trade = maker_trade
        _updating_objects = [order, other_side_order, trade, other_side_trade]
        if order.side == SpotOrderSideChoice.BUY:
            paying_quantity = quote_quantity
        else:
            paying_quantity = filling_quantity        
        if order.locked_amount < paying_quantity:
            raise
        order.locked_amount -= paying_quantity
        # pay to the order side and settle the trade
        other_side_fee_amount, order_rebate = get_trade_fee(
            # is_other_side_maker=is_other_side_maker,
            order=order,
            other_side_order=other_side_order,
            paying_quantity=paying_quantity
        )
        other_side_fee_amount = ZERO
        total_trading_fee = other_side_fee_amount + order_rebate
        paying_quantiy_to_other_sidte = paying_quantity - total_trading_fee
        other_side_trade.received_amount = paying_quantiy_to_other_sidte
        other_side_trade.received_fee = total_trading_fee
        update_objects.add(
            Asset.add_to_asset(
                account=other_side_order.account, token=order.locked_asset.token, 
                quantity=paying_quantiy_to_other_sidte
            )
        )
        trade.paid_amount = paying_quantity
        if other_side_fee_amount > ZERO:
            Income.create(trade=other_side_trade, token=order.locked_asset.token, amount=other_side_fee_amount)
        if order_rebate > ZERO:
            # pay rebate
            update_objects.add(
                Asset.add_to_asset(account=order.account, token=order.locked_asset.token, quantity=order_rebate)
            )
            trade.paid_rebate = order_rebate
        if order.status == OrderStatusChoice.FILLED and order.locked_amount > ZERO:
            # unlock remaning asset after filling order
            update_objects.add(
                Asset.add_to_asset(account=order.account, token=order.locked_asset.token, quantity=order.locked_amount)
            )
            order.locked_amount = '0.0'
        order.filled_quote_quantity += quote_quantity
        order.filled_quantity += filling_quantity
        if (order.quantity > ZERO and order.quantity - order.filled_quantity == ZERO) or (order.quote_quantity > ZERO and order.quote_quantity - order.filled_quote_quantity == ZERO):
            order.status = OrderStatusChoice.FILLED
        for obj in _updating_objects:
            obj.save()
            update_objects.add(obj)
    return update_objects


@atomic
def get_trade_fee(order, other_side_order, paying_quantity):
    # a fee paid order
    if order.fee_rebate > ZERO:
        other_side_fee_amount = ZERO
        order_rebate = ZERO
    else:
        # a rebate maker order
        rebate = -order.fee_rebate
        fee = min(other_side_order.fee_rebate, rebate)
        other_side_fee_amount = paying_quantity * fee
        order_rebate = paying_quantity * rebate
    return other_side_fee_amount, order_rebate


# @atomic
# def get_trade_fee(is_other_side_maker, paying_quantity):
#     # pay to maker
#     if is_other_side_maker:
#         other_side_fee_amount = ZERO
#         order_rebate = ZERO
#     else:
#         # pay to taker
#         other_side_fee_amount = paying_quantity * settings.SPOT_TRADING_FEE
#         order_rebate = paying_quantity * settings.SPOT_MAKER_REBATE
#     return other_side_fee_amount, order_rebate


