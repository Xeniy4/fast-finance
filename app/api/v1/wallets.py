from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database_models import User
from app.dependency import get_current_user_dependence, get_db
from app.schemas import CreateWalletRequest
from app.service import wallets as wallets_service

router = APIRouter()


# Запрос баланса кошелька.
# Имя кошелька(wallet_name) передается в query-параметрах
@router.get("/balance")
def get_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependence),
    wallet_name: str | None = None,
) -> Union[dict[str, int], dict[str, Union[str, int]]]:
    return wallets_service.get_wallet(  # type: ignore[no-any-return]
        db=db, current_user=current_user, wallet_name=wallet_name
    )


# В этом методе имя кошелька(wallet_name) передается в path-параметре
@router.post("/wallets")
def create_wallet(
    wallet: CreateWalletRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependence),
) -> dict[str, Union[str, int]]:
    return wallets_service.create_wallet(  # type: ignore[no-any-return]
        db=db, current_user=current_user, wallet=wallet
    )
