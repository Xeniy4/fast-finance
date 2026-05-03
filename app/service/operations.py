from datetime import datetime
from decimal import Decimal

from fastapi import (
    HTTPException,
)
from sqlalchemy.orm import (
    Session,
)

from app.database_models import User
from app.enum import OperationType
from app.repository import operations as operations_repository
from app.repository import wallets as wallets_repository
from app.schemas import (
    OperationRequest,
    OperationResponse,
)
from app.service.exchange_servise import get_exchange_rate


def add_income(
    db: Session, current_user: User, operation: OperationRequest
) -> OperationResponse:
    # Проверить, существует ли кошелек
    if not wallets_repository.is_wallet_exist(
        db=db, user_id=current_user.id, wallet_name=operation.wallet_name
    ):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found",
        )

    # Добавить доход к балансу
    wallet = wallets_repository.add_income(
        db=db,
        user_id=current_user.id,
        wallet_name=operation.wallet_name,
        amount=operation.amount,
    )
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type=OperationType.INCOME,
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.descriptions,
    )
    db.commit()  # сохранение данного изменения
    # Возвратить информацию об операции
    return OperationResponse.model_validate(operation)


def add_expense(
    db: Session, current_user: User, operation: OperationRequest
) -> OperationResponse:
    # Проверить, существует ли кошелек
    if not wallets_repository.is_wallet_exist(
        db=db, user_id=current_user.id, wallet_name=operation.wallet_name
    ):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found",
        )
    # Проверить достаточно ли средств в кошельке
    wallet = wallets_repository.get_wallet_balance_by_name(
        db=db, user_id=current_user.id, wallet_name=operation.wallet_name
    )
    if wallet.balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. "
            f"Available: {wallet.balance}",  # Недостаточно средств. Доступно:
        )

    # Вычесть расход из баланса
    wallet = wallets_repository.add_expense(
        db=db,
        user_id=current_user.id,
        wallet_name=operation.wallet_name,
        amount=operation.amount,
    )
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type=OperationType.EXPENSE,
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.descriptions,
    )
    db.commit()  # сохранение данного изменения
    # Возвратить информацию об операции
    return OperationResponse.model_validate(operation)


def get_operation_list(
    db: Session,
    current_user: User,
    wallet_id: int | None,
    date_from: datetime,
    date_to: datetime,
) -> list[OperationResponse]:

    if wallet_id:
        wallet = wallets_repository.get_wallet_by_id(
            db=db, user_id=current_user.id, wallet_id=wallet_id
        )
        if not wallet:
            raise HTTPException(
                status_code=404,
                detail=f"Wallet id '{wallet_id}' not found",
            )

        wallet_ids = [wallet.id]
    else:
        wallets = wallets_repository.get_all_wallets(
            db=db,
            user_id=current_user.id,
        )
        wallet_ids = [w.id for w in wallets]

    operations = operations_repository.get_operation_list(
        db=db, wallets_ids=wallet_ids, date_from=date_from, date_to=date_to
    )
    result = []
    for operation in operations:
        result.append(OperationResponse.model_validate(operation))

    return result


def transfer_between_wallets(
    db: Session,
    user_id: int,
    from_wallet_id: int,
    to_wallet_id: int,
    amount: Decimal,
) -> OperationResponse:
    from_wallet = wallets_repository.get_wallet_by_id(
        db=db, user_id=user_id, wallet_id=from_wallet_id
    )
    to_wallet = wallets_repository.get_wallet_by_id(
        db=db, user_id=user_id, wallet_id=to_wallet_id
    )

    if not from_wallet or not to_wallet:  # любой кошелек не найден
        raise HTTPException(404, "Wallet not found")

    if (
        from_wallet.balance < amount
    ):  # Проверка достаточности средств на балансе
        raise HTTPException(
            400,
            f"Not enough money: {from_wallet.balance} {from_wallet.currency}",
        )

    target_amount = amount
    exchange_rate = 1.0  # курс по умолчанию (одинаковые валюты)
    if from_wallet.currency != to_wallet.currency:
        exchange_rate = get_exchange_rate(
            base=from_wallet.currency,  # type: ignore[assignment]
            target=to_wallet.currency,
        )
        target_amount = round(amount * exchange_rate, 2)  # type: ignore

    from_wallet.balance = round(
        from_wallet.balance - amount, 2
    )  # списываем из кошелька
    to_wallet.balance = round(
        to_wallet.balance + target_amount, 2
    )  # зачисляем на другой кошелек
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=from_wallet.id,
        type=OperationType.TRANSFER,
        amount=target_amount,
        currency=from_wallet.currency,
        category="Перевод",
    )
    db.add(from_wallet)
    db.add(to_wallet)
    db.add(operation)
    db.commit()
    return OperationResponse.model_validate(operation)
