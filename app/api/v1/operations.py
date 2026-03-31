from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependency import get_db
from app.service import operations as operation_service

from app.schemas import OperationRequest

router = APIRouter()


@router.post("/operations/income")  # income - доход
def add_income(operation: OperationRequest, db: Session = Depends(get_db)):
    return operation_service.add_income(operation=operation, db=db)


@router.post("/operations/expense")  # expense - расход
def add_expense(operation: OperationRequest, db: Session = Depends(get_db)):
    return operation_service.add_expense(operation=operation, db=db)
