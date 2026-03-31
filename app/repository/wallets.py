from decimal import Decimal

from sqlalchemy.orm import Session

from app.database_models import Wallet


def is_wallet_exist(db: Session, wallet_name: str) -> bool:
    """Проверить наличие кошелька по имени кошелька

    Args:
        db: Сессия БД
        wallet_name: Имя кошелька

    Returns:
        Результат наличия кошелька
    """
    # находим в бд такую запись и проверяем, что этот результат не равен None
    return db.query(Wallet).filter(Wallet.name == wallet_name).first() is not None


def add_income(db: Session, wallet_name: str, amount: Decimal) -> Wallet:
    """Добавить доход в кошелек по имени кошелька

    Args:
        db: Сессия БД
        wallet_name: Имя кошелька
        amount: Количество денег

    Returns:
        Итоговая сумма
    """
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()  # находим в бд такую запись
    wallet.balance += amount
    return wallet  # возвращаем объект модели


def get_wallet_balance_by_name(db: Session, wallet_name: str) -> Wallet:
    """Получить баланс кошелька по имени кошелька

    Args:
        db: Сессия БД
        wallet_name: Имя кошелька

    Returns:
        Сумма баланса кошелька
    """
    return db.query(Wallet).filter(Wallet.name == wallet_name).first()  # находим в бд такую запись


def add_expense(db: Session, wallet_name: str, amount: Decimal) -> Wallet:
    """Добавить расход в кошелек по имени кошелька

    Args:
        db: Сессия БД
        wallet_name: Имя кошелька
        amount: Количество денег

    Returns:
        Итоговая сумма
    """
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()  # находим в бд такую запись
    wallet.balance -= amount
    return wallet  # возвращаем объект модели


def get_all_wallets(db: Session) -> list[Wallet]:
    """Сумма общего баланса (пока хз зачем)
    Args:
        db: Сессия БД

    Returns:
        Сумма
    """
    return db.query(Wallet).all()


def create_wallet(db: Session, wallet_name: str, amount: Decimal) -> Wallet:
    """Создать новый кошелек

    Args:
        db: Сессия БД
        wallet_name: Имя кошелька
        amount: Количество денег

    Returns:
        Итоговая сумма
    """
    wallet = Wallet(name=wallet_name, balance=amount)  # создали объект
    db.add(wallet)  # добавили объект в БД
    db.flush()  # добавляет генерацию нового id
    return wallet
