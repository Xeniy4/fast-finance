from datetime import datetime

from fastapi import (
    HTTPException,
)
from sqlalchemy.orm import (
    Session,
)

from app.database_models import User
from app.repository import operations as operations_repository
from app.repository import wallets as wallets_repository
from app.schemas import (
    OperationRequest,
    OperationResponse,
)


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
        type="income",
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
        type="expense",
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
