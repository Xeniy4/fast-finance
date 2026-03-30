from fastapi import APIRouter
from app.service import operations as operation_service

from app.schemas import OperationRequest

router = APIRouter()


@router.post("/operations/income")  # income - доход
def add_incomes(operation: OperationRequest):
    return operation_service.add_incomes(operation=operation)


@router.post("/operations/expense")  # expense - расход
def add_expense(operation: OperationRequest):
    return operation_service.add_expense(operation=operation)
