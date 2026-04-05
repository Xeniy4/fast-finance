from decimal import Decimal

from sqlalchemy.orm import Session

from app.database_models import Wallet, User


def is_wallet_exist(db: Session, user_id: int, wallet_name: str) -> bool:
    """Проверить наличие кошелька по имени кошелька

    Args:
        db: Сессия БД
        wallet_name: Имя кошелька
        user_id: Идентификатор юзера, за которого происходит запрос

    Returns:
        Результат наличия кошелька
    """
    # находим в бд такую запись и проверяем, что этот результат не равен None
    return db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first() is not None


def add_income(db: Session, user_id: int, wallet_name: str, amount: Decimal) -> Wallet:
    """Добавить доход в кошелек по имени кошелька

    Args:
        db: Сессия БД
        wallet_name: Имя кошелька
        amount: Количество денег
        user_id: Идентификатор юзера, за которого происходит запрос

    Returns:
        Итоговая сумма
    """
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()  # находим в бд такую запись
    wallet.balance += amount
    return wallet  # возвращаем объект модели


def get_wallet_balance_by_name(db: Session, user_id: int, wallet_name: str) -> Wallet:
    """Получить баланс кошелька по имени кошелька

    Args:
        db: Сессия БД
        wallet_name: Имя кошелька
        user_id: Идентификатор юзера, за которого происходит запрос

    Returns:
        Сумма баланса кошелька
    """
    return db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()  # находим в бд такую запись


def add_expense(db: Session, user_id: int, wallet_name: str, amount: Decimal) -> Wallet:
    """Добавить расход в кошелек по имени кошелька

    Args:
        db: Сессия БД
        wallet_name: Имя кошелька
        amount: Количество денег
        user_id: Идентификатор юзера, за которого происходит запрос

    Returns:
        Итоговая сумма
    """
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()  # находим в бд такую запись
    wallet.balance -= amount
    return wallet  # возвращаем объект модели


def get_all_wallets(db: Session, user_id: int) -> list[Wallet]:
    """Сумма общего баланса одного пользователя по всем кошелькам
    Args:
        db: Сессия БД
        user_id: Идентификатор юзера, за которого происходит запрос

    Returns:
        Сумма
    """
    return db.query(Wallet).filter(Wallet.user_id == user_id).all()


def create_wallet(db: Session, user_id: int, wallet_name: str, amount: Decimal) -> Wallet:
    """Создать новый кошелек

    Args:
        db: Сессия БД
        wallet_name: Имя кошелька
        amount: Количество денег
        user_id: Идентификатор юзера, за которого происходит запрос

    Returns:
        Итоговая сумма
    """
    wallet = Wallet(name=wallet_name, balance=amount, user_id=user_id)  # создали объект
    db.add(wallet)  # добавили объект в БД
    db.flush()  # добавляет генерацию нового id
    return wallet
