"""
Тут содержатся зависимости. Например, для создания подключения к БД.
Работает отдаленно как фикстуры. Только тут код выполняется внутри,
а выполнение до и после указывается в функции зависимости

"""
from typing import Generator

from sqlalchemy.orm import Session

from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    # происходит подключение к бд
    db = SessionLocal()
    try:
        yield db # весь код функции должен выполняться здесь
    finally:
        db.close() # бд отключается