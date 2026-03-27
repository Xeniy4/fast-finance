from email.policy import default
# from http.client import HTTPException

from fastapi import FastAPI, HTTPException

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
@app.post("/wallets/{name}")
def receive_money(name: str, amount: int): # receive - получить
    # Если кошелька с таким именем еще нет - создаем его с балансом 0
    if name not in BALANCE:
        BALANCE[name] = 0 # создали кошелек с балансом 0
    # Если кошелек существует - добавляем сумму к балансу кошелька
    BALANCE[name] += amount
    # Возвращаем информацию об операции
    return {
        "message": f"Added {amount} to {name}",
        "wallet": name,
        "new_balance": BALANCE[name]
    }
