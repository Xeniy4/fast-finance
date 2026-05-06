from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from sqlalchemy.orm import Session

from app.database_models import (
    User,
)
from app.dependency import (
    get_current_user_dependence,
    get_db,
)
from app.schemas import (
    OperationRequest,
    OperationResponse,
    TransferCreateSchema,
)
from app.service import operations as operation_service

router = APIRouter()


@router.post("/operations/income", response_model=OperationResponse)
def add_income(
    operation: OperationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependence),
) -> OperationResponse:
    return operation_service.add_income(
        db=db, current_user=current_user, operation=operation
    )


@router.post("/operations/expense", response_model=OperationResponse)
def add_expense(
    operation: OperationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependence),
) -> OperationResponse:
    return operation_service.add_expense(
        db=db, current_user=current_user, operation=operation
    )


@router.get("/operations", response_model=list[OperationResponse])
def get_operations_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependence),
    wallet_id: int | None = Query(None),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
) -> list[OperationResponse]:
    return operation_service.get_operation_list(
        db=db,
        current_user=current_user,
        wallet_id=wallet_id,
        date_from=date_from,  # type: ignore[arg-type]
        date_to=date_to,  # type: ignore[arg-type]
    )


@router.post("/operations/transfer", response_model=OperationResponse)
async def create_transfer(
    payload: TransferCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependence),
) -> OperationResponse:
    return await operation_service.transfer_between_wallets(
        db=db,
        user_id=current_user.id,
        from_wallet_id=payload.from_wallet_id,
        to_wallet_id=payload.to_wallet_id,
        amount=payload.amount,
    )
