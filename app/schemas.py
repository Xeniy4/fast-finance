from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)
from pydantic_core.core_schema import FieldValidationInfo

from app.enum import CurrencyEnum


class OperationRequest(BaseModel):
    wallet_name: str = Field(
        ..., max_length=127
    )  # ... (называется Ellipsis) - значит поле обязательно в заполнении)
    amount: Decimal
    descriptions: str | None = Field(
        None, max_length=255
    )  # поле не обязательно к заполнению и дефолтное значение None

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
    initial_balance: Decimal = Decimal(0)
    currency: CurrencyEnum = CurrencyEnum.RUB

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


class UsersRequest(BaseModel):
    login: str = Field(..., max_length=100)


class UsersResponse(UsersRequest):
    model_config = {
        "from_attributes": True
    }  # преобразовывает модель БД в pydantic модель

    id: int


class WalletResponse(BaseModel):  # может быть лучше CreateWalletResponse
    model_config = {"from_attributes": True}

    id: int
    name: str
    balance: Decimal
    currency: CurrencyEnum


class OperationResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    wallet_id: int
    type: str
    amount: Decimal
    currency: CurrencyEnum
    category: str | None = None
    subcategory: str | None = None
    created_at: datetime


class TransferCreateSchema(BaseModel):
    from_wallet_id: int
    to_wallet_id: int
    amount: Decimal

    @field_validator("to_wallet_id")
    @classmethod
    def wallets_must_differ(
        cls, v: int, info: FieldValidationInfo
    ) -> int:  # валидация отличия id кошельков, т.к.
        # нельзя переводить в тот же кошелек
        if "from_wallet_id" in info.data and v == info.data["from_wallet_id"]:
            raise ValueError("Same wallets ids!")
        return v

    @field_validator("amount")
    def amount_zero(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("Amount can`t be negative")
        return v
