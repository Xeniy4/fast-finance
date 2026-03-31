from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependency import get_db
from app.schemas import CreateWalletRequest
from app.service import wallets as wallets_service

router = APIRouter()


# Запрос баланса кошелька. Имя кошелька(wallet_name) передается в query-параметрах
@router.get("/balance")
def get_balance(wallet_name: str | None = None, db: Session = Depends(get_db)):
    return wallets_service.get_wallet(wallet_name=wallet_name, db=db)


# В этом методе имя кошелька(wallet_name) передается в path-параметре
@router.post("/wallets")
def create_wallet(wallet: CreateWalletRequest, db: Session = Depends(get_db)):
    return wallets_service.create_wallet(wallet=wallet, db=db)
