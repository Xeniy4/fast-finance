import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base
from app.dependency import get_db
from main import app
from fastapi.testclient import TestClient


TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# Функция для получения сессии БД через dependency injection в FastApi
def get_test_db() -> Generator[Session, None, None]:
    # происходит подключение к бд
    db = TestSessionLocal()
    try:
        yield db  # весь код функции должен выполняться здесь
    finally:
        db.close()  # бд отключается


app.dependency_overrides[get_db] = get_test_db  # dependency_overrides функция заменяется на указанную

@pytest.fixture()
def client():
    yield TestClient(app) # Объект TestClient создается относительно объекта app. Нужно для того, чтобы фикстура "подхватилась".


@pytest.fixture(autouse=True)
def setup_db():
    """Очищает БД для каждого теста"""
    Base.metadata.create_all(bind=test_engine)  # создает тестовую таблицу
    yield
    Base.metadata.drop_all(bind=test_engine)  # удаляет тестовую таблицу


@pytest.fixture(autouse=True)
def db_session() -> Generator[Session, None, None]:
    """Подключение к БД в тесте"""
    db = TestSessionLocal()
    try:
        yield db  # весь код функции должен выполняться здесь
    finally:
        db.close()  # бд отключается



