from masks import masked_card_number, masked_account_number

def masked_numbers(card_or_account: str) -> str:
    """Функция принимает данные карты или счета и маскирует часть их номера"""

    if card_or_account[:4] == "Счет":
        return f"{card_or_account[:5]}{masked_account_number(card_or_account[5:])}"
    return f"{card_or_account[:-16]}{masked_card_number(card_or_account[-16:])}"



#тестирование
if __name__ in '__main__':
    test_data = ["Maestro 1596837868705199",
                    "Счет 64686473678894779589",
                    "MasterCard 7158300734726758",
                    "Счет 35383033474447895560",
                    "Visa Classic 6831982476737658",
                    "Visa Platinum 8990922113665229",
                    "Visa Gold 5999414228426353",
                    "Счет 73654108430135874305"]

    for data in test_data:
        print(masked_numbers(data))
