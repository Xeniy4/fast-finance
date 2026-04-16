import http
from tests.helpers.data_tests import (
    gen_random_amount,
    gen_random_str,
)
from tests.helpers.endpoints import Endpoints


def test_create_wallet_auth(create_user, client):
    """
    Проверка возможности создания кошелька авторизированным пользователем.
    Шаги:
        1. Отправить post запрос на эндпоинт "/api/v1/wallets"
        2. В теле ответа передать валидные значения
        3. В авторизации передать токен
    ОР: Кошелек создан, данные ответа соответствуют ожидаемым значениям.
    """
    balance = gen_random_amount(0, 300)
    wallet_name = gen_random_str()
    response = client.post(
        url=Endpoints.create_wallet.value,
        json={"name":wallet_name,
              "initial_balance": balance},
        headers={"Authorization": f"Bearer {create_user.login}"}
    )

    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["message"] == f"Wallet '{wallet_name}' created"
    assert response.json()["wallet"] == wallet_name
    assert response.json()["new_balance"] == balance


def test_create_wallet_no_auth(client):
    """
    Проверка отсутствия возможности создания кошелька не авторизированным пользователем.
    Шаги:
        1. Отправить post запрос на эндпоинт "/api/v1/wallets"
        2. В теле ответа передать валидные значения
        3. В авторизации не передавать токен
    ОР: Код ответа 401.
    """
    balance = gen_random_amount(0, 300)
    wallet_name = gen_random_str()
    response = client.post(
        url=Endpoints.create_wallet.value,
        json={"name":wallet_name,
              "initial_balance": balance}
    )

    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"


def test_create_exist_wallet(create_user, client):
    """
    Проверка отсутствия возможности повторного создания существующего кошелька.
    Шаги:
        1. Отправить post запрос на эндпоинт "/api/v1/wallets"
        2. В теле ответа передать валидные значения
        3. В авторизации передать токен
        4. Повторно отправить post запрос на эндпоинт "/api/v1/wallets" с тем же значением name
        5. В теле ответа передать существующее значение кошелька
    ОР: Код ответа 400. Ошибка, второй кошелек не создан.
    """
    balance = gen_random_amount(0, 300)
    wallet_name = gen_random_str()
    response_valid_wallet = client.post(
        url=Endpoints.create_wallet.value,
        json={"name":wallet_name,
              "initial_balance": balance},
        headers={"Authorization": f"Bearer {create_user.login}"}
    )

    assert response_valid_wallet.status_code == http.HTTPStatus.OK
    assert response_valid_wallet.json()["message"] == f"Wallet '{wallet_name}' created"
    assert response_valid_wallet.json()["wallet"] == wallet_name
    assert response_valid_wallet.json()["new_balance"] == balance

    response_no_valid_wallet = client.post(
        url=Endpoints.create_wallet.value,
        json={"name":wallet_name,
              "initial_balance": balance},
        headers={"Authorization": f"Bearer {create_user.login}"}
    )
    assert response_no_valid_wallet.status_code == http.HTTPStatus.BAD_REQUEST
    assert response_no_valid_wallet.json()["detail"] == f"Wallet '{wallet_name}' already exist"


def test_create_wallet_no_balance(create_user, client):
    """
    Проверка возможности создания кошелька без баланса.
    Шаги:
        1. Отправить post запрос на эндпоинт "/api/v1/wallets"
        2. В теле ответа передать валидные значения, поле initial_balance не передавать
        3. В авторизации передать токен
    ОР: Кошелек создан, данные ответа соответствуют ожидаемым значениям.
    """
    wallet_name = gen_random_str()
    response = client.post(
        url=Endpoints.create_wallet.value,
        json={"name":wallet_name},
        headers={"Authorization": f"Bearer {create_user.login}"}
    )

    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["message"] == f"Wallet '{wallet_name}' created"
    assert response.json()["wallet"] == wallet_name
    assert response.json()["new_balance"] == 0
