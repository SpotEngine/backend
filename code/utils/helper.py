from decimal import Decimal, ROUND_DOWN, localcontext, ROUND_UP, getcontext, ROUND_FLOOR, ROUND_CEILING
from django.conf import settings
import math
from .enums import ZERO, SystemGeneratedEvent

class DecimalRound:
    @classmethod
    def round_down(cls, decimal: Decimal, decimal_places=settings.BASE_MODEL_DECIMAL_PLACES, sample=None):
        return cls.round_decimal(method=ROUND_FLOOR, decimal=decimal, decimal_places=decimal_places, sample=sample)
    
    @classmethod
    def round_up(cls, decimal: Decimal, decimal_places=settings.BASE_MODEL_DECIMAL_PLACES, sample=None):
        return cls.round_decimal(method=ROUND_CEILING, decimal=decimal, decimal_places=decimal_places, sample=sample)

    @classmethod
    def round_decimal(cls, method, decimal: Decimal, decimal_places=settings.BASE_MODEL_DECIMAL_PLACES, sample=None):
        if sample:
            decimal_places = -(math.floor(math.log10(sample)))
        decimal_places += len(str(abs(int(decimal))))
        with localcontext() as context:
            context.prec = decimal_places
            context.rounding = method
            result = decimal / Decimal("1")
        return result


def ifnone2zero(value):
    if value == None:
        value = ZERO
    return value

class SystemEvent:
    def __init__(self, event: SystemGeneratedEvent, data: dict):
        self.event = event
        self.data = data
