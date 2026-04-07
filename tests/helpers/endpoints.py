from enum import Enum


class Endpoints(Enum):
    operations_expense = "/api/v1/operations/expense"
    operations_income = "/api/v1/operations/income"
    balance = "/api/v1/balance"
