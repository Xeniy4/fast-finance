from sqlalchemy.orm import Session

from app.database_models import User


def get_user(db: Session, login: str) -> User | None:
    """Получить информацию о пользователе по логину

    Args:
        db: Сессия БД
        login: Логин пользователя

    Returns:
        User: модель ответа с полями пользователя из БД
    """
    return (
        db.query(User).filter(User.login == login).scalar()
    )  # находим в бд такую запись.
    # .scalar() - алхимия(бд) преобразовывает результат своего запроса в результат экземпляра класса User


def create_user(db: Session, login: str) -> User:
    """Создать пользователя

    Args:
        db: Сессия БД
        login: Логин пользователя

    Returns:
        User: модель ответа с полями пользователя из БД
    """
    user = User(login=login)
    db.add(user)  # добавляет логин в таблицу user
    db.flush()  # добавляет записи в таблице user id
    return user
