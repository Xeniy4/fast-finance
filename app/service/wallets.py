from fastapi import HTTPException

from app.schemas import CreateWalletRequest
from app.repository import wallets as wallets_repository


def get_wallet(wallet_name: str | None = None): # у него wallet, а у нас изначально было написано get_balanse
    # Если имя кошелька не указано (None) - считаем общий баланс
    if wallet_name is None:
        wallets = wallets_repository.get_all_wallets()
        return {"total_balance": sum(wallets.values())} # сумма всех значений
    # Если имя указано - проверяем существует ли запрашиваемый кошелек
    if not wallets_repository.is_wallet_exist(wallet_name=wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )
    # Если кошелек существует - возвращаем баланс
    balance = wallets_repository.get_wallet_balance_by_name(wallet_name=wallet_name)
    return {"wallet":wallet_name, "balance": balance}


def create_wallet(wallet: CreateWalletRequest):
    # Проверяем не существует ли такой же кошелек
    if wallets_repository.is_wallet_exist(wallet_name=wallet.name):
        raise HTTPException(
            status_code=400,
            detail= f"Wallet '{wallet.name}' already exist"
        )
    # Если не существует, то создаем новый с начальным балансом
    new_balance = wallets_repository.create_wallet(wallet_name=wallet.name, amount=wallet.initial_balance)
    # Возвращаем инфу о созданном кошельке
    return {
      "message": f"Wallet '{wallet.name}' created",
      "wallet": wallet.name,
      "new_balance": new_balance
    }