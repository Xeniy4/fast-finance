import http

from app.database_models import User, Wallet
from tests.helpers.data_tests import (
    gen_random_amount,
    gen_random_str,
    get_random_name,
)
from tests.helpers.endpoints import Endpoints


def test_add_expense_success(db_session, client):
    """
    Проверка возможности списания средств
    Предусловия:
        Создать тестовые данные (логин, начальный баланс, сумма, описание, имя кошелька)
    Шаги:
        1. Создать юзера и добавить в БД
        2. Создать кошелек и добавить в БД
        3. Отправить post запрос на эндпоинт "/api/v1/operations/expense"
        4. Проверить данные в ответе
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
    db_session.commit()
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
            "descriptions": descriptions,
        },
        headers={"Authorization": f"Bearer {user.login}"},
    )

    # Assert
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["message"] == "Expense added"
    assert response.json()["wallet"] == wallet.name
    assert response.json()["amount"] == amount
    assert response.json()["description"] == descriptions
    assert response.json()["new_balance"] == expect_balance


def test_add_expense_not_enough_balance(
    create_user_wallet, create_user, client
):
    """
    Проверка отсутствия возможности списания суммы больше, чем в балансе
    Предусловия:
        Создать тестовые данные (логин, начальный баланс, сумма, описание, имя кошелька)
    Шаги:
        1. Создать юзера и добавить в БД
        2. Создать кошелек и добавить в БД
        3. Отправить post запрос на эндпоинт "/api/v1/operations/expense"
            В теле запроса отправить отрицательное значение поля amount
        4. Проверить данные в ответе
    ОР: Запрос неуспешный, код ответа 400
    """
    # Arrange
    amount = gen_random_amount(400, 500)
    descriptions = gen_random_str()
    # Act
    response = client.post(
        url=Endpoints.operations_expense.value,
        json={
            "wallet_name": create_user_wallet.name,
            "amount": amount,
            "descriptions": descriptions,
        },
        headers={"Authorization": f"Bearer {create_user.login}"},
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_add_expense_empty_wallet_name(
    create_user_wallet, create_user, client
):
    """
    Проверка отсутствия возможности списания суммы из кошелька без поля имени кошелька
    Предусловия:
        Создать тестовые данные (логин, начальный баланс, сумма, описание, имя кошелька)
    Шаги:
        1. Создать юзера и добавить в БД
        2. Создать кошелек и добавить в БД
        3. Отправить post запрос на эндпоинт "/api/v1/operations/expense"
            В теле запроса отправить пустое значение поля wallet_name
        4. Проверить данные в ответе
    ОР: Запрос неуспешный, код ответа 422
    """
    # Arrange
    descriptions = gen_random_str()
    amount = gen_random_amount(1, 100)

    # Act
    response = client.post(
        url=Endpoints.operations_expense.value,
        json={
            "wallet_name": "  ",
            "amount": amount,
            "descriptions": descriptions,
        },
        headers={"Authorization": f"Bearer {create_user.login}"},
    )
    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY


def test_add_expense_wallet_not_exist(create_user_wallet, create_user, client):
    """
    Проверка отсутствия возможности списания суммы из несуществующего кошелька
    Предусловия:
        Создать тестовые данные (логин, имя кошелька, описание)
    Шаги:
        1. Создать юзера и добавить в БД
        2. Отправить post запрос на эндпоинт "/api/v1/operations/expense"
            В теле запроса отправить несуществующее значение поля wallet_name
        4. Проверить данных в ответе
    ОР: Запрос неуспешный, код ответа 404
    """
    # Arrange
    wallet_name = get_random_name()
    descriptions = gen_random_str()
    amount = gen_random_amount(1, 100)

    # Act
    response = client.post(
        url=Endpoints.operations_expense.value,
        json={
            "wallet_name": wallet_name,
            "amount": amount,
            "descriptions": descriptions,
        },
        headers={"Authorization": f"Bearer {create_user.login}"},
    )
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_add_expense_negative_amount(create_user_wallet, create_user, client):
    """
    Проверка отсутствия возможности списания отрицательной суммы из кошелька
    Предусловия:
        Создать тестовые данные (логин, начальный баланс, сумма, описание, имя кошелька)
    Шаги:
        1. Создать юзера и добавить в БД
        2. Создать кошелек и добавить в БД
        3. Отправить post запрос на эндпоинт "/api/v1/operations/expense"
            В теле запроса отправить отрицательное значение поля amount
        4. Проверить данные в ответе
    ОР: Запрос неуспешный, код ответа 400
    """
    # Arrange
    descriptions = gen_random_str()

    # Act
    response = client.post(
        url=Endpoints.operations_expense.value,
        json={
            "wallet_name": create_user_wallet.name,
            "amount": -20,
            "descriptions": descriptions,
        },
        headers={"Authorization": f"Bearer {create_user.login}"},
    )
    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY


def test_add_expense_unauthorized(client):
    """
    Проверка отсутствия возможности списания суммы без авторизации
    Предусловия:
        Создать тестовые данные (имя кошелька, сумма, описание)
    Шаги:
        1. Создать юзера и добавить в БД
        2. Отправить post запрос на эндпоинт "/api/v1/operations/expense"
            В теле запроса отправить валидные поля без авторизации.
        4. Проверить данных в ответе
    ОР: Запрос неуспешный, код ответа 401
    """
    # Arrange
    wallet_name = get_random_name()
    descriptions = gen_random_str()
    amount = gen_random_amount(1, 100)

    # Act
    response = client.post(
        url=Endpoints.operations_expense.value,
        json={
            "wallet_name": wallet_name,
            "amount": amount,
            "descriptions": descriptions,
        },
        headers={"Authorization": "Bearer notexists"},
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
