import pytest

from src.masks import masked_account_number, masked_card_number


@pytest.fixture
def account_number():
    return "73654108430135874305"


@pytest.fixture
def card_number():
    return "7000792289606361"


def test_masked_account_number(account_number):
    assert masked_account_number(account_number) == "**4305"


def test_masked_card_number(card_number):
    assert masked_card_number(card_number) == "7000 79** **** 6361"


def test_masked_card_number_error(card_number):
    with pytest.raises(Exception) as ex:
        masked_card_number("card_number")
    assert str(ex.value) == "Передан неверный формат карты"

    with pytest.raises(Exception) as ex:
        masked_card_number("12345678")
    assert str(ex.value) == "Передан неверный формат карты"


def test_masked_account_number_error(account_number):
    with pytest.raises(Exception) as ex:
        masked_account_number("account_number")
    assert str(ex.value) == "Передан неверный формат счета"

    with pytest.raises(Exception) as ex:
        masked_account_number("12345678")
    assert str(ex.value) == "Передан неверный формат счета"
