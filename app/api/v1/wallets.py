from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database_models import User
from app.dependency import get_db, get_current_user
from app.schemas import CreateWalletRequest
from app.service import wallets as wallets_service

router = APIRouter()


# Запрос баланса кошелька. Имя кошелька(wallet_name) передается в query-параметрах
@router.get("/balance")
def get_balance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), wallet_name: str | None = None):
    return wallets_service.get_wallet(db=db, current_user=current_user, wallet_name=wallet_name)


# В этом методе имя кошелька(wallet_name) передается в path-параметре
@router.post("/wallets")
def create_wallet(wallet: CreateWalletRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return wallets_service.create_wallet(db=db, current_user=current_user, wallet=wallet) # тут он не добавил current_user 1:40:27
