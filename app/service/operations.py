from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database_models import User
from app.repository import wallets as wallets_repository
from app.schemas import OperationRequest


def add_income(db: Session, current_user: User, operation: OperationRequest):
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
    db.commit()  # сохранение данного изменения
    # Возвратить информацию об операции
    return {
        "message": "Income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.descriptions,
        "new_balance": wallet.balance,
    }


def add_expense(db: Session, current_user: User, operation: OperationRequest):
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
    db.commit()  # сохранение данного изменения
    # Возвратить информацию об операции
    return {
        "message": "Expense added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.descriptions,
        "new_balance": wallet.balance,
    }
