from enum import StrEnum, auto


class CurrencyEnum(StrEnum):
    RUB = auto()  # значение подставится автоматически "rub"
    USD = auto()
    EUR = auto()
