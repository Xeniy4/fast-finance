from app.schemas import OperationRequest
from fastapi import HTTPException
from app.repository import wallets as wallets_repository


def add_income(operation: OperationRequest):
    # Проверить, существует ли кошелек
    if not wallets_repository.is_wallet_exist(wallet_name=operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )

    # Добавить доход к балансу
    new_balance = wallets_repository.add_income(wallet_name=operation.wallet_name, amount=operation.amount)

    # Возвратить информацию об операции
    return {
      "message": "Income added",
      "wallet": operation.wallet_name,
      "amount": operation.amount,
      "description": operation.descriptions,
      "new_balance": new_balance
    }


def add_expense(operation: OperationRequest):
    # Проверить, существует ли кошелек
    if not wallets_repository.is_wallet_exist(wallet_name=operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )
    # Проверить достаточно ли средств в кошельке
    balance = wallets_repository.get_wallet_balance_by_name(wallet_name=operation.wallet_name)
    if balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. "
                   f"Available: {balance}" # Недостаточно средств. Доступно:
        )

    # Вычесть расход из баланса
    new_balance = wallets_repository.add_expense(wallet_name=operation.wallet_name, amount=operation.amount)
    # Возвратить информацию об операции
    return {
      "message": "Expense added",
      "wallet": operation.wallet_name,
      "amount": operation.amount,
      "description": operation.descriptions,
      "new_balance": new_balance
    }
