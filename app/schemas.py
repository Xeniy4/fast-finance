from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)  # ... (называется Ellipsis) - значит поле обязательно в заполнении)
    amount: Decimal
    descriptions: str | None = Field(None, max_length=255)  # поле не обязательно к заполнению и дефолтное значение None

    # Валидация, что поле положительное
    @field_validator('amount')
    def amount_must_be_positive(cls, value: Decimal) -> Decimal:
        # Проверить, что значение больше 0
        if value <= 0:
            raise ValueError("Amount must be positive")
        # Вернуть значение
        return value


    # Удаление лишних пробелов по бокам
    @field_validator('wallet_name')
    def wallet_name_not_empty(cls, value: str) -> str:
        # Убрать пробелы побокам
        value = value.strip()
        # Убедиться, что строка не пустая
        if not value:
            raise ValueError("Wallet name cannot be empty")

        # Вернуть значение
        return value


class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: Decimal = 0


    # Удаление лишних пробелов по бокам
    @field_validator('name')
    def name_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value

    # Валидация, что баланс не отрицательный
    @field_validator('initial_balance')
    def balance_not_negative(cls, value: Decimal) -> Decimal:
        if value < 0:
            raise ValueError("initial balance cannot be negative")
        return value
