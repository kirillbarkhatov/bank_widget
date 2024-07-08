from unittest.mock import patch

import pytest

from src.external_api import currency_converter


def test_currency_converter():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"rates": {"RUB": 100}}
        assert currency_converter(1, "USD") == 100.00


def test_currency_converter_exception():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 201
        with pytest.raises(Exception):
            assert currency_converter(1, "USD")
