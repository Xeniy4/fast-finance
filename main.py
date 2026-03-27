from fastapi import FastAPI, HTTPException
from models.operations_models import OperationRequest, CreateWalletRequest

"""
запуск сервера через команду в терминале:

uvicorn main:app --reload

main - путь к нашему файлу
app - инстанс класса
--reload - параметр, который перезапустит сервер
закрыть сервер Ctrl+C
"""

app = FastAPI()

# Словарь для хранения баланса
# Ключ - название кошелька, значение - баланс
BALANCE = {}


# Запрос баланса кошелька. Имя кошелька(wallet_name) передается в query-параметрах
@app.get("/balance")
def get_balance(wallet_name: str | None = None):
    # Если имя кошелька не указано (None) - считаем общий баланс
    if wallet_name is None:
        return {"total_balance": sum(BALANCE.values())} # сумма всех значений
    # Если имя указано - проверяем существует ли запрашиваемый кошелек
    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )
    # Если кошелек существует - возвращаем баланс
    return {"wallet":wallet_name, "balance": BALANCE[wallet_name]}


# В этом методе имя кошелька(wallet_name) передается в path-параметре
@app.post("/wallets")
def create_wallet(wallet: CreateWalletRequest):
    # Проверяем не существует ли такой же кошелек
    if wallet.name in BALANCE:
        raise HTTPException(
            status_code=400,
            detail= f"Wallet '{wallet.name}' already exist"
        )
    # Если не существует, то создаем новый с начальным балансом
    BALANCE[wallet.name] = wallet.initial_balance
    # Возвращаем инфу о созданном кошельке
    return {
      "message": f"Wallet '{wallet.name}' created",
      "wallet": wallet.name,
      "new_balance": BALANCE[wallet.name]
    }


@app.post("/operations/income") # income - доход
def add_incomes(operation: OperationRequest):
    # Проверить, существует ли кошелек
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )

    # Добавить доход к балансу
    BALANCE[operation.wallet_name] += operation.amount

    # Возвратить информацию об операции
    return {
      "message": "Income added",
      "wallet": operation.wallet_name,
      "amount": operation.amount,
      "description": operation.descriptions,
      "new_balance": BALANCE[operation.wallet_name]
    }


@app.post("/operations/expense") # expense - расход
def add_expense(operation: OperationRequest):
    # Проверить, существует ли кошелек
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )
    # Проверить достаточно ли средств в кошельке
    if BALANCE[operation.wallet_name] < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. "
                   f"Available: {BALANCE[operation.wallet_name]}" # Недостаточно средств. Доступно:
        )


    # Вычесть расход из баланса
    BALANCE[operation.wallet_name] -= operation.amount

    # Возвратить информацию об операции
    return {
      "message": "Expense added",
      "wallet": operation.wallet_name,
      "amount": operation.amount,
      "description": operation.descriptions,
      "new_balance": BALANCE[operation.wallet_name]
    }