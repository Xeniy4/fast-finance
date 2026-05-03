from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.database_models import Operation
from app.enum import CurrencyEnum


def create_operation(
    db: Session,
    wallet_id: int,
    type: str,
    amount: Decimal,
    currency: CurrencyEnum,
    category: str | None = None,
    subcategory: str | None = None,
) -> Operation:
    """Создание операции и сохранение ее в БД

    Args:
        db: Сессия БД
        wallet_id: id кошелька
        type: Тип операции (доход/расход)
        amount: Сумма операции
        currency: Валюта
        category: Категория
        subcategory: Подкатегория

    Returns:
        Operation: модель ответа с полями операции из БД
    """
    operation = Operation(
        wallet_id=wallet_id,
        type=type,
        amount=amount,
        currency=currency,
        category=category,
        subcategory=subcategory,
    )
    db.add(operation)
    db.flush()
    return operation


def get_operation_list(
    db: Session,
    wallets_ids: list[int],
    date_from: datetime | None,
    date_to: datetime | None,
) -> list[Operation]:
    query = db.query(Operation).filter(Operation.wallet_id.in_(wallets_ids))

    if date_from:
        query = query.filter(Operation.created_at >= date_from)

    if date_to:
        query = query.filter(Operation.created_at <= date_to)

    return query.all()
