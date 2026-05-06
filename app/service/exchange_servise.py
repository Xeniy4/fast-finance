from decimal import Decimal

import aiohttp

from app.enum import CurrencyEnum

# Захардкожено для случая, когда внешний сервис не отвечает.

FALLBACK_RATES: dict[tuple[str, str], Decimal] = {
    (CurrencyEnum.USD, CurrencyEnum.RUB): Decimal(str(95.0)),
    (CurrencyEnum.USD, CurrencyEnum.EUR): Decimal(str(0.92)),
    (CurrencyEnum.EUR, CurrencyEnum.RUB): Decimal(str(103.26)),
    (CurrencyEnum.RUB, CurrencyEnum.USD): Decimal(str(0.0105)),
    (CurrencyEnum.EUR, CurrencyEnum.USD): Decimal(str(0.87)),
    (CurrencyEnum.RUB, CurrencyEnum.EUR): Decimal(str(0.0097)),
}


async def get_exchange_rate(
    base: CurrencyEnum, target: CurrencyEnum
) -> Decimal:
    """Получение курса обмена между двумя валютами

    Args:
        base: Базовая валюта
        target: Целевая валюта

    Returns:
        Курс обмена (сколько единиц целевой валюты за 1 базовую)
        Если курс не найден - возвращается 1 (без конвертации)
    """
    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json"  # noqa: E501

    aio_timeout = aiohttp.ClientTimeout(total=5.0)

    try:

        async with aiohttp.ClientSession(timeout=aio_timeout) as session:
            async with session.get(url=url) as response:
                response.raise_for_status()  # если не 200, будет отбрасывать exception # noqa: E501
                # await должен появиться на обработке результатов запроса
                data = await response.json()
                base_map = data.get(base, {})
                rate = base_map.get(target)

        if rate is not None and isinstance(rate, (int, float)):
            return Decimal(rate)
        raise KeyError("Rate not found")

    except Exception:
        return FALLBACK_RATES.get((base, target), Decimal(1))
