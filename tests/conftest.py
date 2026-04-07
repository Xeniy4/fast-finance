import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from sqlalchemy.orm import Session
from app.database import Base
from app.database_models import User, Wallet
from app.dependency import get_db
from main import app
from fastapi.testclient import TestClient
import logging
from tests.helpers.utils import LoggingClient
from tests.helpers.data_tests import get_random_name, gen_random_amount

logger = logging.getLogger(__name__)

TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def pytest_configure():
    # Отключение логирования для Faker
    faker_logger = logging.getLogger("faker")
    faker_logger.disabled = True
    logging.getLogger("faker.factory").disabled = True
    logging.getLogger("faker.generator").disabled = True



@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield LoggingClient(test_client)

# Функция для получения сессии БД через dependency injection в FastApi
def get_test_db() -> Generator[Session, None, None]:
    # происходит подключение к бд
    db = TestSessionLocal()
    try:
        yield db  # весь код функции должен выполняться здесь
    finally:
        db.close()  # бд отключается


app.dependency_overrides[get_db] = get_test_db  # dependency_overrides функция заменяется на указанную

# @pytest.fixture()
# def client():
#     yield TestClient(app) # Объект TestClient создается относительно объекта app. Нужно для того, чтобы фикстура "подхватилась".


@pytest.fixture(scope="session")
def setup_db():
    """Очищает БД для каждого теста"""
    Base.metadata.create_all(bind=test_engine)  # создает тестовую таблицу
    yield
    Base.metadata.drop_all(bind=test_engine)  # удаляет тестовую таблицу


# @pytest.fixture(autouse=True)
@pytest.fixture
def db_session(setup_db) -> Generator[Session, None, None]:
    """Подключение к БД в тесте"""
    db = TestSessionLocal()
    try:
        yield db  # весь код функции должен выполняться здесь
    finally:
        db.close()  # бд отключается


@pytest.fixture(autouse=True)
def create_user(db_session) -> Generator[User, None, None]:
    user_login = get_random_name()
    user = User(login=user_login)
    db_session.add(user)
    db_session.flush()
    db_session.commit()
    yield user
    # удаляем пользователя после теста
    db_session.delete(user)
    db_session.commit()


@pytest.fixture
def create_user_wallet(
        create_user: User,
        db_session: Session
) -> Generator[Wallet, None, None]:
    """
    Создание кошелька для указанного пользователя.
    Параметры:
        create_user: пользователь, для которого создаётся кошелёк
        db_session: сессия БД.
    Возвращает: объект Wallet.
    """
    balance = gen_random_amount(100, 200)
    wallet_name = get_random_name()

    wallet = Wallet(
        name=wallet_name,
        balance=balance,
        user_id=create_user.id
    )
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(instance=wallet)
    yield wallet
    # Удаление кошелька после теста
    db_session.delete(wallet)
    db_session.commit()