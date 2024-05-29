def masked_card_number(card_number: int) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску формате XXXX XX** **** XXXX"""

    return f"{str(card_number)[:4]} {str(card_number)[4:6]}** **** {str(card_number)[-4:]}"


def masked_account_number(account_number: int) -> str:
    """Функция принимает на вход номер счета и возвращает его маску в формате **XXXX"""

    return f"**{str(account_number)[-4:]}"


# для проверки
# print(masked_card_number(7000792289606361))
# print(masked_account_number(73654108430135874305))
