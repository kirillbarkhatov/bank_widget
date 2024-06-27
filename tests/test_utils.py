from pathlib import Path
from unittest.mock import patch

import pytest

from src.utils import get_transaction_amount, get_transactions_from_json


@pytest.fixture
def path_file_success():
    return str(Path.cwd().joinpath("data", "operations.json"))


@pytest.fixture
def path_file_failure():
    return str(Path.cwd().joinpath("data", "failure_test.json"))


# Тест при условии существования файла
def test_get_transactions_from_json_file_exist(path_file_success):

    # содержимое файла в ожидаемом формате
    with patch("json.load") as mock_transactions:
        mock_transactions.return_value = [{"test_key": "test_value"}]
        assert get_transactions_from_json(path_file_success) == [{"test_key": "test_value"}]

    # содержимое файла не соответствуют формату
    with patch("json.load") as mock_transactions:
        mock_transactions.return_value = "test"
        assert get_transactions_from_json(path_file_success) == []

    # содержимое файла отсутствует
    with patch("json.load") as mock_transactions:
        mock_transactions.return_value = ""
        assert get_transactions_from_json(path_file_success) == []


# Тест при условии отсутствия файла
def test_get_transactions_from_json_file_failure(path_file_failure):
    assert get_transactions_from_json(path_file_failure) == []


@pytest.mark.parametrize(
    "transaction, amount",
    [
        ({"operationAmount": {"amount": "31957.58", "currency": {"code": "RUB"}}}, 31957.58),
        ({"operationAmount": {"amount": "433.11", "currency": {"code": "RUB"}}}, 433.11),
    ],
)
def test_get_transaction_amount_rub(transaction, amount):
    assert get_transaction_amount(transaction) == amount


@pytest.fixture
def transaction_usd():
    return {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560",
    }


def test_get_transaction_amount_currency(transaction_usd):
    with patch("src.external_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"rates": {"RUB": 100}}
        assert get_transaction_amount(transaction_usd) == 822137.00

    with pytest.raises(Exception) as ex:
        get_transaction_amount("transaction_usd")
    assert str(ex.value) == "Не удалось обработать транзакцию - проверьте формат данных"
