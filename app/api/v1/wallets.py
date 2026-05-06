from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.database_models import User
from app.dependency import (
    get_current_user_dependence,
    get_db,
)
from app.schemas import (
    CreateWalletRequest,
    TotalBalanceResponse,
    WalletResponse,
)
from app.service import wallets as wallets_service

router = APIRouter()


# Запрос баланса кошелька.
# Имя кошелька(wallet_name) передается в query-параметрах
@router.get("/balance")
async def get_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependence),
) -> TotalBalanceResponse:
    return await wallets_service.get_total_balance(
        db=db, current_user=current_user
    )


# В этом методе имя кошелька(wallet_name) передается в path-параметре
@router.post("/wallets", response_model=WalletResponse)
def create_wallet(
    wallet: CreateWalletRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependence),
) -> WalletResponse:
    return wallets_service.create_wallet(
        db=db, current_user=current_user, wallet=wallet
    )


# Запрос списка кошельков пользователя
@router.get("/list/wallets", response_model=list[WalletResponse])
def get_all_wallets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependence),
) -> list[WalletResponse]:
    return wallets_service.get_list_wallets(db=db, current_user=current_user)
