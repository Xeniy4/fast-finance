import http
from tests.conftest import create_user_wallet
from tests.helpers.endpoints import Endpoints

from tests.helpers.data_tests import get_random_name


def test_get_balance(create_user_wallet, create_user, client):
    """
    Проверка возможности получения баланса
    Шаги:
        1. Отправить post запрос на эндпоинт "/api/v1/balance"
        2. Проверить данные в ответе
    ОР: Данные ответа соответствуют ожидаемым значениям, код ответа 200.
    """
    response = client.get(
        url=Endpoints.balance.value,
        params={"wallet_name":create_user_wallet.name},
        headers={"Authorization": f"Bearer {create_user.login}"}
    )
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["wallet"] == create_user_wallet.name
    assert response.json()["balance"] == create_user_wallet.balance


def test_get_balance_no_wallet(create_user_wallet, create_user, client):
    """
    Проверка возможности получения баланса без указания кошелька
    Шаги:
        1. Отправить post запрос на эндпоинт "/api/v1/balance"
        2. Проверить данные в ответе
    ОР: В ответе отображается общий баланс, код ответа 200.
    """
    response = client.get(
        url=Endpoints.balance.value,
        headers={"Authorization": f"Bearer {create_user.login}"}
    )
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["total_balance"] == create_user_wallet.balance


def test_get_balance_unauthorized(client):
    """
    Проверка отсутствия возможности получения баланса без авторизации
    Шаги:
        1. Отправить post запрос на эндпоинт "/api/v1/balance"
        2. Проверить данные в ответе
    ОР: Запрос неуспешный, код ответа 401
    """
    wallet_name = get_random_name()
    response = client.get(
        url=Endpoints.balance.value,
        params={"wallet_name":wallet_name},
        headers={"Authorization": f"Bearer notexists"}
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED


def test_get_balance_wallet_not_exist(create_user, client):
    """
    Проверка отсутствия возможности получения баланса из несуществующего кошелька
    Шаги:
        1. Отправить post запрос на эндпоинт "/api/v1/balance"
        2. Проверить данные в ответе
    ОР: Данные ответа соответствуют ожидаемым значениям, код ответа 200.
    """
    wallet_name = get_random_name()
    response = client.get(
        url=Endpoints.balance.value,
        params={"wallet_name":wallet_name},
        headers={"Authorization": f"Bearer {create_user.login}"}
    )
    print(f"resp = {response}")
    assert response.status_code == http.HTTPStatus.NOT_FOUND
