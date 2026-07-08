from decimal import Decimal, ROUND_HALF_UP

MONEY_PRECISION = Decimal('0.01')

def to_money(value) -> Decimal:
    if value is None:
        return Decimal('0.00')
    return Decimal(str(value)).quantize(MONEY_PRECISION, rounding=ROUND_HALF_UP)
