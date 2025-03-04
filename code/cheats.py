from decimal import Decimal, ROUND_DOWN, localcontext, ROUND_UP, getcontext, ROUND_FLOOR, ROUND_CEILING

def round_decimal(method, decimal: Decimal, decimal_places=3, sample=None):
    # if sample:
    #     decimal_places = -(math.floor(math.log10(sample)))
    decimal_places += len(str(abs(int(decimal))))
    with localcontext() as context:
        context.prec = decimal_places
        context.rounding = method
        result = decimal / Decimal("1")
    return result

round_decimal(ROUND_DOWN, Decimal("123.12345678"), 4)