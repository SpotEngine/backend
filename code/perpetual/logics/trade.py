from utils.choices import OrderStatusChoice, PerpOrderTypeChoice, PositionStatusChoice, PerpDirectionChoice
from ..models import Order, Income, Trade, Position, PerpetualWallet
from django.db.transaction import atomic
from utils.enums import ZERO, SystemGeneratedEvent
from .cancel import cancel_order
from utils.helper import DecimalRound, ifnone2zero, SystemEvent
from django.conf import settings
from django.db.models import Sum, F, When, Case, Q
from .release_lock import release
from ..trader.serializers import PerpLimitOrderSerializer, PerpOrderSerializer
from uuid import uuid4


def get_filling_size(taker: Order, maker: Order):
    maker_max_trade_size = maker.size - maker.filled_size
    if taker.type == PerpOrderTypeChoice.LIMIT:
        taker_max_trade_size = taker.size - taker.filled_size
    elif taker.type == PerpOrderTypeChoice.MARKET:
        if taker.reduce_only:
            taker_max_trade_size = taker.size - taker.filled_size
        else:
            taker_max_quote_quantity = taker.quote_quantity - taker.filled_quote_quantity
            taker_max_trade_size = ZERO
            lot_steps = int(maker_max_trade_size/maker.contract.lot_size) + 1
            for i in range(lot_steps):
                taker_size_candidate = maker_max_trade_size - i * maker.contract.lot_size
                if taker_max_quote_quantity >= taker_size_candidate * maker.price:
                    taker_max_trade_size = taker_size_candidate
                    break
    filling_size = max(min(taker_max_trade_size, maker_max_trade_size), ZERO)
    return filling_size


def increase_position_size(trade: Trade, order: Order, updated_objects: set, fee_portion, rebate_portion, rebate_amount, size):
    if size > ZERO:
        _result = Position.increase_position_size(
            account=trade.order.account, 
            trade=trade,
            contract=trade.order.contract,
            size=size,
            direction=order.direction,
            leverage=order.leverage,
            fee_portion=fee_portion,
            rebate_portion=rebate_portion,
        )
        position = _result['position']
        received_rebate = _result['received_rebate']
        paid_fee = _result['paid_fee']

        updated_objects.add(position)
        rebate_amount += received_rebate

        if paid_fee > ZERO:
            if order.locked.fee >= paid_fee:
                trade.paid_fee += paid_fee
                order.locked.fee -= paid_fee
                order.locked.save()
            else:
                raise Exception('Not enough locked fee to pay trading fee!')
    return updated_objects, size, rebate_amount


def reduce_position_size(opposite_direction: PerpDirectionChoice, trade: Trade, order: Order, updated_objects: set, trading_token, fee_portion, rebate_portion, rebate_amount, size):
    try:
        position = Position.objects.select_for_update().get(
            account=trade.order.account, 
            contract=trade.order.contract,
            status=PositionStatusChoice.OPEN,
            direction=opposite_direction,
        )
    except Position.DoesNotExist:
        position = None
    if position:
        updated_objects.add(position)
        _result = position.reduce_position_size(trade=trade, fee_portion=fee_portion, rebate_portion=rebate_portion)
        reduction_size = _result['reduction_size']
        adding_quantity = _result['adding_quantity']
        received_rebate = _result['received_rebate']
        paid_fee = _result['paid_fee']
        rebate_amount += received_rebate
        size -= reduction_size
        updated_objects.add(
            PerpetualWallet.add_to_asset(
                account=order.account, token=trading_token, 
                quantity=adding_quantity-paid_fee,
            )
        )
        trade.paid_fee += paid_fee
        trade.save()
    return updated_objects, size, rebate_amount


@atomic
def create_trade(taker: Order, maker: Order, match_tag: str):
    filling_size = get_filling_size(taker=taker, maker=maker)
    if filling_size == ZERO:
        return None
    trading_token = maker.contract.margin
    trade_kwargs = {
        'contract': maker.contract,
        'price': maker.price,
        'size': filling_size,
        'match_tag': match_tag,
        'paid_token': trading_token,
    }
    taker_trade = Trade.create(order=taker, is_maker=False, **trade_kwargs)
    maker_trade = Trade.create(order=maker, is_maker=True, **trade_kwargs)

    updated_objects = set([maker])
    updated_objects = liquid_positions(maker, updated_objects)
    for is_maker in [True, False]:
        if is_maker:
            order = maker
            trade = maker_trade
            opposite_direction = taker.direction
        else:
            order = taker
            trade = taker_trade
            opposite_direction = maker.direction
        _updating_objects = [order, trade]
        size = filling_size

        trade_margin_amount = maker.price * filling_size / order.leverage
        trade_margin_amount = DecimalRound.round_up(trade_margin_amount)
        if order.locked.asset:
            if order.locked.amount < trade_margin_amount:
                raise
            else:
                order.locked.amount -= trade_margin_amount
        else:
            if order.locked.size < size:
                raise
            else:
                order.locked.size -= size            
        order.locked.save()
        # pay to the order side and settle the trade
        fee_portion, rebate_portion = get_trade_fee(
            is_maker=is_maker,
        )
        rebate_amount = ZERO
        updated_objects, size, rebate_amount = reduce_position_size(
            opposite_direction=opposite_direction,
            trade=trade,
            order=order,
            updated_objects=updated_objects,
            trading_token=trading_token,
            fee_portion=fee_portion,
            rebate_portion=rebate_portion,
            rebate_amount=rebate_amount,
            size=size
        )
        updated_objects, size, rebate_amount = increase_position_size(
            trade=trade,
            order=order,
            updated_objects=updated_objects,
            fee_portion=fee_portion,
            rebate_portion=rebate_portion,
            rebate_amount=rebate_amount,
            size=size
        )
        if rebate_amount > ZERO:
            # pay rebate_amount
            updated_objects.add(
                PerpetualWallet.add_to_asset(
                    account=order.account, 
                    token=trading_token, 
                    quantity=rebate_amount
                )
            )
            trade.received_rebate = rebate_amount
        order.filled_quote_quantity += trade_margin_amount * order.leverage # TODO for market add , status not filled after fill
        order.filled_size += filling_size
        if (order.size > ZERO and order.size - order.filled_size == ZERO) or (order.quote_quantity > ZERO and order.quote_quantity - order.filled_quote_quantity == ZERO) :
            order.status = OrderStatusChoice.FILLED
            updated_asset = release(order.locked)
            if updated_asset:
                updated_objects.add(updated_asset)
        for obj in _updating_objects:
            obj.save()
            updated_objects.add(obj)
    income_amount = taker_trade.paid_fee - maker_trade.received_rebate
    if income_amount > ZERO:
        Income.create(trade=taker_trade, token=trading_token, amount=income_amount)
    check_consistency(maker)
    return updated_objects

def check_consistency(maker):
    pnl_query = Position.objects.filter(
        contract=maker.contract, 
        status=PositionStatusChoice.OPEN,
    ).annotate(
        price_diff= maker.price - F("entry_price")
    ).annotate(
        new_pnl=Case(
            When(direction=PerpDirectionChoice.LONG, then=F("price_diff") * F("size")),
            When(direction=PerpDirectionChoice.SHORT, then= -1 * F("price_diff") * F("size")),
        )
    )
    validate_sufficient_margin_for_profits(pnl_query=pnl_query, maker=maker)
    validate_no_loss_more_than_margin_in_position(pnl_query=pnl_query)
    pnl_query.update(pnl=F("new_pnl"))

def validate_no_loss_more_than_margin_in_position(pnl_query):
    liquidated_positions = pnl_query.filter(new_pnl__lt=ZERO, margin_amount__lt= -1 * F("new_pnl"))
    if liquidated_positions.exists():
        raise Exception("loss_more_than_margin_in_position")


def validate_sufficient_margin_for_profits(pnl_query, maker: Order):
    # new_pnl_status = pnl_query.aggregate(
    #     profit_sum=Sum(
    #         Case(
    #             When(new_pnl__gte=ZERO, then=F("new_pnl")),
    #             default=ZERO
    #         ),
    #     ),
    #     margin_sum=Sum(
    #         Case(
    #             When(new_pnl__lt=ZERO, then=F("margin_amount")),
    #             default=ZERO
    #         ),
    #     )
    # )
    # profit_sum = ifnone2zero(new_pnl_status["profit_sum"])
    # margin_sum = ifnone2zero(new_pnl_status["margin_sum"])
    # margin_sum += maker.contract.margin_amount
    # if margin_sum  < profit_sum:
    #     raise Exception(f'insufficient_margin_for_profits')
    new_pnl_status = pnl_query.filter(new_pnl__gte=ZERO).aggregate(
        profit_sum=Sum(
            "new_pnl"
        ),
        margin_sum=Sum("margin_amount"),
    )
    # print("new_pnl_status:", new_pnl_status)
    profit_sum = ifnone2zero(new_pnl_status["profit_sum"])
    margin_sum = ifnone2zero(new_pnl_status["margin_sum"])
    if maker.contract.margin_amount < profit_sum + margin_sum:
        raise Exception(f'insufficient_margin_for_profits')


@atomic
def get_trade_fee(is_maker):
    fee_portion = ZERO if is_maker else settings.PERPETUAL_TAKER_FEE
    rebate_portion = settings.PERPETUAL_MAKER_REBATE if is_maker else ZERO
    return fee_portion, rebate_portion


def liquid_positions(maker: Order, updated_objects: set):
    positions = Position.objects.filter(
        Q(direction=PerpDirectionChoice.LONG, liquidation_price__gte=maker.price) | Q(direction=PerpDirectionChoice.SHORT, liquidation_price__lte=maker.price),
        status=PositionStatusChoice.OPEN, 
        contract=maker.contract, 
    )
    for position in positions:
        updated_objects = cancel_open_orders(position, updated_objects)
        updated_objects = trigger_liquidation_order(position, updated_objects)
        position.status = PositionStatusChoice.LIQUDATION
        position.save()
        updated_objects.add(position)
    return updated_objects


def cancel_open_orders(position, updated_objects):
    order_locks = position.orderlock_set.filter(size__gt=ZERO)
    for order_lock in order_locks:
        orders = order_lock.order_set.filter(status__in=[OrderStatusChoice.PLACED, OrderStatusChoice.RECEIVED])
        for order in orders:
            updated_objects = cancel_order(order, updated_objects=updated_objects)
    return updated_objects


def trigger_liquidation_order(position: Position, updated_objects: set):
    account_id = position.account_id
    serializer = PerpLimitOrderSerializer(
        data={
            'client_order_id': str(uuid4()),
            'contract': position.contract,
            'direction': PerpDirectionChoice.SHORT if position.direction == PerpDirectionChoice.LONG else PerpDirectionChoice.LONG,
            'price': position.hard_liquidation_price,
            'size': position.size,
            'reduce_only': True
        }, 
        context={'account_id': account_id}
    )
    serializer.is_valid(raise_exception=True)
    order = serializer.save(**{'liquidation': True, 'account_id': account_id})
    order_serializer = PerpOrderSerializer(instance=order)
    order_data = order_serializer.data
    order_data['account_id'] = account_id
    li_order = SystemEvent(event=SystemGeneratedEvent.LIQUIDATION_ORDER, data=order_data)
    updated_objects.add(li_order)
    return updated_objects

