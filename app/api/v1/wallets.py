from fastapi import APIRouter
from app.schemas import CreateWalletRequest
from app.service import wallets as wallets_service

router = APIRouter()


# Запрос баланса кошелька. Имя кошелька(wallet_name) передается в query-параметрах
@router.get("/balance")
def get_balance(wallet_name: str | None = None):
    return wallets_service.get_wallet(wallet_name=wallet_name)


# В этом методе имя кошелька(wallet_name) передается в path-параметре
@router.post("/wallets")
def create_wallet(wallet: CreateWalletRequest):
    return wallets_service.create_wallet(wallet=wallet)
