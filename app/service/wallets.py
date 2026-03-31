from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas import CreateWalletRequest
from app.repository import wallets as wallets_repository


def get_wallet(db: Session, wallet_name: str | None = None):
    # Если имя кошелька не указано (None) - считаем общий баланс
    if wallet_name is None:
        wallets = wallets_repository.get_all_wallets(db=db)
        return {"total_balance": sum([w.balance for w in wallets])}  # сумма всех значений
    # Если имя указано - проверяем существует ли запрашиваемый кошелек
    if not wallets_repository.is_wallet_exist(db=db, wallet_name=wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )
    # Если кошелек существует - возвращаем баланс
    wallet = wallets_repository.get_wallet_balance_by_name(db=db, wallet_name=wallet_name)
    return {"wallet": wallet.name, "balance": wallet.balance}


def create_wallet(db: Session, wallet: CreateWalletRequest):
    # Проверяем не существует ли такой же кошелек
    if wallets_repository.is_wallet_exist(db=db, wallet_name=wallet.name):
        raise HTTPException(
            status_code=400,
            detail=f"Wallet '{wallet.name}' already exist"
        )
    # Если не существует, то создаем новый с начальным балансом
    wallet = wallets_repository.create_wallet(db=db, wallet_name=wallet.name, amount=wallet.initial_balance)
    db.commit()
    # Возвращаем инфу о созданном кошельке
    return {
        "message": f"Wallet '{wallet.name}' created",
        "wallet": wallet.name,
        "new_balance": wallet.balance
    }
