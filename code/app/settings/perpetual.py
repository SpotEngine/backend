import os
from decimal import Decimal


PERPETUAL_MATCH_ENGINE_ORDER_SELECT_SIZE = 100
PERPETUAL_MAKER_REBATE = Decimal('0.005')
PERPETUAL_TRADING_FEE = Decimal('0.01')
PERPETUAL_TAKER_FEE = PERPETUAL_MAKER_REBATE + PERPETUAL_TRADING_FEE
