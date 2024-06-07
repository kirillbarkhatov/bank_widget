from datetime import datetime

from src.masks import masked_account_number, masked_card_number


def masked_numbers(card_or_account: str) -> str:
    """Функция принимает данные карты или счета и маскирует часть их номера"""

    if card_or_account[:4] == "Счет":
        return f"{card_or_account[:5]}{masked_account_number(int(card_or_account[5:]))}"
    return f"{card_or_account[:-16]}{masked_card_number(int(card_or_account[-16:]))}"


def convert_date(date_iso: str) -> str:
    """Функция вернет дату в формате ДД.ММ.ГГГГ"""

    date = datetime.strptime(date_iso, "%Y-%m-%dT%H:%M:%S.%f")
    return datetime.strftime(date, "%d.%m.%Y")


# тестирование
# if __name__ in "__main__":
#     test_data = [
#         "Maestro 1596837868705199",
#         "Счет 64686473678894779589",
#         "MasterCard 7158300734726758",
#         "Счет 35383033474447895560",
#         "Visa Classic 6831982476737658",
#         "Visa Platinum 8990922113665229",
#         "Visa Gold 5999414228426353",
#         "Счет 73654108430135874305",
#     ]
#
#     for data in test_data:
#         print(masked_numbers(data))
#
#     test_date = "2018-07-11T02:26:18.671407"
#     print(convert_date(test_date))
