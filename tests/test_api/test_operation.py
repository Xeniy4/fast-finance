import http

from app.database_models import User, Wallet
from tests.helpers.endpoints import Endpoints

from tests.helpers.data_tests import gen_random_amount, get_random_name, gen_random_str


def test_add_expense_success(db_session, client):
    """
    Проверка возможности списания средств
    Предусловия:
        Создать тестовые данные (логин, начальный баланс, сумма, описание, имя кошелька)
    Шаги:
        1. Создать юзера и добавить в БД
        2. Создать кошелек и добавить в БД
        3. Отправить post запрос на эндпоинт "/api/v1/operations/expense" для списания суммы
        4. Проверить данных в ответе
    ОР: Данные ответа соответствуют данным из запроса, сумма в балансе обновилась
    """
    # Arrange
    user_login = get_random_name()
    balance = gen_random_amount(200, 400)
    wallet_name = get_random_name()
    descriptions = gen_random_str()
    amount = gen_random_amount(1, 100)
    expect_balance = balance - amount

    user = User(login=user_login)
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name=wallet_name, balance=balance, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(instance=wallet)

    # Act
    response = client.post(
        url=Endpoints.operations_expense.value,
        json={  # через модель OperationRequest не получилось реализовать, тк у json проблемы с типом Decimal
            "wallet_name": wallet.name,
            "amount": amount,
            "descriptions": descriptions
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )

    # Assert
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["message"] == "Expense added"
    assert response.json()["wallet"] == wallet.name
    assert response.json()["amount"] == amount
    assert response.json()["description"] == descriptions
    assert response.json()["new_balance"] == expect_balance


def test_add_expense_negative_amount(db_session, client):
    """
    Проверка отсутствия возможности списания отрицательной суммы из кошелька
    Предусловия:
        Создать тестовые данные (логин, начальный баланс, сумма, описание, имя кошелька)
    Шаги:
        1. Создать юзера и добавить в БД
        2. Создать кошелек и добавить в БД
        3. Отправить post запрос на эндпоинт "/api/v1/operations/expense" для списания суммы.
            В теле запроса отправить отрицательное значение
        4. Проверить данных в ответе
    ОР: Данные ответа соответствуют данным из запроса, сумма в балансе обновилась
    """
    # Arrange
    user_login = get_random_name()
    balance = gen_random_amount(100, 199)
    wallet_name = get_random_name()
    descriptions = gen_random_str()
    amount = gen_random_amount(200, 300)
    expect_balance = balance - amount

    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    balance = 200
    wallet = Wallet(name="card", balance=balance, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(instance=wallet)

    # Act
    response = client.post(
        url=Endpoints.operations_expense.value,
        json={
            "wallet_name": wallet.name,
            "amount": amount,
            "descriptions": descriptions
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST

