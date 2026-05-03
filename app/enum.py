from enum import (
    StrEnum,
    auto,
)


class CurrencyEnum(StrEnum):
    RUB = auto()  # значение подставится автоматически "rub"
    USD = auto()
    EUR = auto()


class OperationType(StrEnum):
    EXPENSE = auto()
    INCOME = auto()
    TRANSFER = auto()
