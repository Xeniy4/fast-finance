from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database_models import User
from app.enum import CurrencyEnum
from app.repository import wallets as wallets_repository
from app.schemas import (
    CreateWalletRequest,
    TotalBalanceResponse,
    WalletResponse,
)
from app.service import exchange_servise


async def get_total_balance(
    db: Session, current_user: User
) -> TotalBalanceResponse:
    # Если имя кошелька не указано (None) - считаем общий баланс
    wallets = wallets_repository.get_all_wallets(
        db=db, user_id=current_user.id
    )
    total_balance = Decimal(0)
    for wallet in wallets:
        if wallet.currency == CurrencyEnum.RUB:
            total_balance += wallet.balance
        else:
            exchange_rate = await exchange_servise.get_exchange_rate(
                base=wallet.currency, target=CurrencyEnum.RUB
            )
            total_balance += exchange_rate * wallet.balance

    return TotalBalanceResponse(total_balance=total_balance)


def create_wallet(
    db: Session, current_user: User, wallet: CreateWalletRequest
) -> WalletResponse:
    # Проверяем не существует ли такой же кошелек
    if wallets_repository.is_wallet_exist(
        db=db, user_id=current_user.id, wallet_name=wallet.name
    ):
        raise HTTPException(
            status_code=400, detail=f"Wallet '{wallet.name}' already exists"
        )
    # Если не существует, то создаем новый с начальным балансом
    wallet = wallets_repository.create_wallet(
        db=db,
        user_id=current_user.id,
        wallet_name=wallet.name,
        amount=wallet.initial_balance,
        currency=wallet.currency,
    )
    db.commit()
    # Возвращаем инфу о созданном кошельке
    return WalletResponse.model_validate(wallet)


def get_list_wallets(db: Session, current_user: User) -> list[WalletResponse]:
    wallets = wallets_repository.get_all_wallets(
        db=db, user_id=current_user.id
    )
    return [WalletResponse.model_validate(wallet) for wallet in wallets]
