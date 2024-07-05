from pathlib import Path
from unittest.mock import patch

import pytest

from src.utils import (get_transaction_amount, get_transactions_from_csv, get_transactions_from_json,
                       get_transactions_from_xls)


@pytest.fixture
def path_file_success():
    return str(Path.cwd().joinpath("data", "operations.json"))


@pytest.fixture
def path_file_csv_success():
    return str(Path.cwd().joinpath("data", "transactions.csv"))


@pytest.fixture
def path_file_xlsx_success():
    return str(Path.cwd().joinpath("data", "transactions_excel.xlsx"))


@pytest.fixture
def path_file_failure():
    return str(Path.cwd().joinpath("data", "failure_test.json"))


# @pytest.fixture
# def transactions_df():
#     transactions = {'id': [650703, 3598919, 593027, 366176, 5380041],
#             'state': ['EXECUTED', 'EXECUTED', 'CANCELED', 'EXECUTED', 'CANCELED'],
#             'date': ['2023-09-05T11:30:32Z', '2020-12-06T23:00:58Z', '2023-07-22T05:02:01Z', '2020-08-02T09:35:18Z',
#                      '2021-02-01T11:54:58Z'], 'amount': [16210.0, 29740.0, 30368.0, 29482.0, 23789.0],
#             'currency_name': ['Sol', 'Peso', 'Shilling', 'Rupiah', 'Peso'],
#             'currency_code': ['PEN', 'COP', 'TZS', 'IDR', 'UYU'],
#             'from': ['Счет 58803664561298323391', 'Discover 3172601889670065', 'Visa 1959232722494097',
#                      'Discover 0325955596714937', 'Discover 0325955596714937'],
#             'to': ['Счет 39745660563456619397', 'Discover 0720428384694643', 'Visa 6804119550473710',
#                    'Visa 3820488829287420', 'Счет 23294994494356835683'],
#             'description': ['Перевод организации', 'Перевод с карты на карту', 'Перевод с карты на карту',
#                             'Перевод с карты на карту', 'Открытие вклада']}
#     return pd.DataFrame(transactions)


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
def test_get_transactions_from_file_failure(path_file_failure):
    assert get_transactions_from_json(path_file_failure) == []
    assert get_transactions_from_csv(path_file_failure) == []
    assert get_transactions_from_xls(path_file_failure) == []


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


def test_get_transactions_from_csv(path_file_csv_success):
    assert get_transactions_from_csv(path_file_csv_success)[0]["id"] == 650703


def test_get_transactions_from_xlsx(path_file_xlsx_success):
    assert get_transactions_from_xls(path_file_xlsx_success)[0]["id"] == 650703
