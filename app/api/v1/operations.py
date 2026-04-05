from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database_models import User
from app.dependency import get_db, get_current_user
from app.service import operations as operation_service

from app.schemas import OperationRequest

router = APIRouter()


@router.post("/operations/income")  # income - доход
def add_income(operation: OperationRequest, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    return operation_service.add_income(db=db, current_user=current_user, operation=operation)


@router.post("/operations/expense")  # expense - расход
def add_expense(operation: OperationRequest, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    return operation_service.add_expense(db=db, current_user=current_user, operation=operation)
