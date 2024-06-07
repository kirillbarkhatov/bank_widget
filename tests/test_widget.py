import pytest

from src.widget import convert_date, masked_numbers


@pytest.mark.parametrize(
    "number, masked_number",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_masked_numbers(number, masked_number):
    assert masked_numbers(number) == masked_number


@pytest.mark.parametrize(
    "date_input, date_output",
    [
        ("2018-07-11T02:26:18.671407", "11.07.2018"),
        ("2024-07-11T02:26:18.671407", "11.07.2024"),
        ("2018-12-11T02:26:18.671407", "11.12.2018"),
    ],
)
def test_convert_date(date_input, date_output):
    assert convert_date(date_input) == date_output
