from decimal import Decimal

from app.enum import CurrencyEnum

# Захардкожено временно.

FALLBACK_RATES: dict[tuple[str, str], Decimal] = {
    (CurrencyEnum.USD, CurrencyEnum.RUB): Decimal(str(95.0)),
    (CurrencyEnum.USD, CurrencyEnum.EUR): Decimal(str(0.92)),
    (CurrencyEnum.EUR, CurrencyEnum.RUB): Decimal(str(103.26)),
    (CurrencyEnum.RUB, CurrencyEnum.USD): Decimal(str(0.0105)),
    (CurrencyEnum.EUR, CurrencyEnum.USD): Decimal(str(0.87)),
    (CurrencyEnum.RUB, CurrencyEnum.EUR): Decimal(str(0.0097)),
}


def get_exchange_rate(base: CurrencyEnum, target: CurrencyEnum) -> Decimal:
    return FALLBACK_RATES.get((base, target), Decimal(1))
