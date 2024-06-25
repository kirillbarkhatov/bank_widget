from pathlib import Path
from unittest.mock import patch

import pytest

from src.utils import get_transactions_from_json


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
