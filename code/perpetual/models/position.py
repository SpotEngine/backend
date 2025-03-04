from django.db import models
from decimal import Decimal
from utils.enums import ZERO
from utils.helper import ifnone2zero
from utils.base_models import BaseModel, base_decimal
from utils.choices import PositionStatusChoice, PerpDirectionChoice, MarginModeChoice, PositionModeChoice
from django.db.models import Sum
from utils.helper import DecimalRound, ifnone2zero


class Position(BaseModel):
    account = models.ForeignKey("aaa.Account", on_delete=models.PROTECT, null=True, blank=True)
    contract = models.ForeignKey("Contract", on_delete=models.PROTECT, null=True, blank=True)
    
    status = models.CharField(default=PositionStatusChoice.OPEN, max_length=15, choices=PositionStatusChoice.choices, null=True, blank=True)
    direction = models.CharField(default=PerpDirectionChoice.LONG, max_length=5, choices=PerpDirectionChoice.choices, null=True, blank=True)
    margin = models.CharField(default=MarginModeChoice.ISOLATED, max_length=20, choices=MarginModeChoice.choices, null=True, blank=True)
    mode = models.CharField(default=PositionModeChoice.ONEWAY, max_length=20, choices=PositionModeChoice.choices, null=True, blank=True)

    margin_amount = base_decimal()
    leverage = base_decimal()
    size = base_decimal()
    entry_price = base_decimal()
    liquidation_price = base_decimal()
    hard_liquidation_price = base_decimal()
    exit_price = base_decimal()
    pnl = base_decimal(non_negative=False)

    class Meta:
        indexes = [
            models.Index(fields=['contract', 'status', ]),
        ]

    def save(self, *args, **kwargs):
        if self.margin_amount > ZERO and self.status == PositionStatusChoice.OPEN:
            position_value = self.margin_amount * self.leverage
            entry_price = position_value / self.size
            liquidation_trigger_factor = 1
            liquidation_threshold = self.contract.liquidation_threshold
            # self.leverage = DecimalRound.round_up(entry_price / self.margin_amount)
            if self.direction == PerpDirectionChoice.LONG:
                round_method = DecimalRound.round_up
                liquidation_trigger_factor += liquidation_threshold
                position_value -= self.margin_amount
            else:
                round_method = DecimalRound.round_down
                liquidation_trigger_factor -= liquidation_threshold
                position_value += self.margin_amount    
            self.entry_price = round_method(entry_price, sample=self.contract.tick_size)
            liquidation_trigger_factor = Decimal(str(liquidation_trigger_factor))
            self.hard_liquidation_price = round_method(position_value / self.size, sample=self.contract.tick_size)
            self.liquidation_price = round_method(self.hard_liquidation_price * liquidation_trigger_factor, sample=self.contract.tick_size)
        return super().save(*args, **kwargs)

    @property
    def locked_size(self):
        _locked_size = self.orderlock_set.all().aggregate(locked_size=Sum('size'))
        return ifnone2zero(_locked_size["locked_size"])

    @property
    def free_size(self):
        return self.size - self.locked_size

    @classmethod
    def increase_position_size(cls, account, trade, contract, size, direction, leverage, fee_portion, rebate_portion):
        position, _ = Position.objects.select_for_update().get_or_create(
            account=account,
            contract=contract,
            status=PositionStatusChoice.OPEN,
            direction=direction,
            defaults={'leverage': leverage}
        )
        trade_value = size * trade.price
        add_to_margin = trade_value / leverage
        paid_fee = trade_value * fee_portion
        received_rebate = trade_value * rebate_portion
        position.size += size
        position.margin_amount += add_to_margin
        trade.paid_amount += add_to_margin
        print(f'adding to contract margin: {trade.contract.margin_amount} {add_to_margin}')
        trade.contract.margin_amount += add_to_margin
        trade.contract.save()
        trade.save()
        position.save()
        _result = {
            'position': position,
            'received_rebate': received_rebate,
            'paid_fee': paid_fee,
        }
        return _result

    def reduce_position_size(self, trade, fee_portion, rebate_portion):
        reduction_size = min(self.size, trade.size)
        reduction_size_ratio = trade.size / self.size
        self.size -= reduction_size
        trade_value = reduction_size * trade.price 
        if self.direction == PerpDirectionChoice.LONG:
            price_diff = trade.price - self.entry_price
        else:
            price_diff = self.entry_price - trade.price
        _pnl = price_diff * reduction_size
        if _pnl >= ZERO:
            pnl = DecimalRound.round_up(_pnl)
        else:
            pnl = DecimalRound.round_down(_pnl)
        withdraw_from_margin = reduction_size_ratio * self.margin_amount
        withdraw_from_margin = DecimalRound.round_down(withdraw_from_margin)
        if self.size == ZERO:
            self.status = PositionStatusChoice.CLOSED
            if self.margin_amount > withdraw_from_margin:
                withdraw_from_margin = self.margin_amount
        if self.margin_amount < withdraw_from_margin:
            print(self.direction, self.entry_price, self.size, trade.price, trade.size)
            raise
        if pnl < ZERO:
            if abs(pnl) > withdraw_from_margin:
                print(self.direction, self.entry_price, self.size, trade.price, trade.size)
                raise
        #     trade.contract.margin_amount += abs(pnl)
        # else:
        #     if trade.contract.margin_amount > pnl:
        #         trade.contract.margin_amount -= pnl
        #     else:
        #         pass
        # trade.contract.save()

        # self.pnl += pnl
        self.margin_amount -= withdraw_from_margin
        self.save()
        paid_fee = trade_value * fee_portion
        received_rebate = trade_value * rebate_portion
        trade.received_amount += withdraw_from_margin + pnl
        print(f'reducing from contract margin: {trade.contract.margin_amount} {withdraw_from_margin + pnl}')
        trade.contract.margin_amount -= withdraw_from_margin + pnl
        trade.contract.save()
        trade.save()
        adding_quantity = withdraw_from_margin - paid_fee + pnl
        _resuts = {
            'adding_quantity': adding_quantity,
            'received_rebate': received_rebate,
            'paid_fee': paid_fee,
            'reduction_size': reduction_size,
        }
        return _resuts
