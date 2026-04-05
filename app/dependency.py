"""
Тут содержатся зависимости. Например, для создания подключения к БД.
Работает отдаленно как фикстуры. Только тут код выполняется внутри,
а выполнение до и после указывается в функции зависимости
далее
Sequrity object - это структура, которая описывает какой тип авторизации описывает для доступа к ресурсу.
Создают, чтобы четко определить правила доступа: токены, ключи и т.п.
"""
from typing import Generator

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.database_models import User
from app.repository import users as users_repository

sequrity = HTTPBearer()



#Функция для получения сессии БД через dependency injection в FastApi
def get_db() -> Generator[Session, None, None]:
    # происходит подключение к бд
    db = SessionLocal()
    try:
        yield db # весь код функции должен выполняться здесь
    finally:
        db.close() # бд отключается


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(sequrity),
                     db: Session = Depends(get_db)) -> User:
    login = credentials.credentials
    user = users_repository.get_user(db=db,login=login)

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorised")

    return user