import logging

# Настройки логгирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(f"logs/{__name__}.log", mode="w")
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def masked_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску формате XXXX XX** **** XXXX"""

    if type(card_number) is str and len(card_number) == 16 and card_number.isdigit():
        mask_card_number = f"{str(card_number)[:4]} {str(card_number)[4:6]}** **** {str(card_number)[-4:]}"
        logger.info(f"Выполнено маскирование номера карты {card_number}- результат: {mask_card_number}")
        return mask_card_number
    logger.error(f"Не удалось выполнить маскирование номера карты - передан неверный формат карты: {card_number}")
    raise Exception("Передан неверный формат карты")


def masked_account_number(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску в формате **XXXX"""

    if type(account_number) is str and len(account_number) == 20 and account_number.isdigit():
        mask_account_number = f"**{str(account_number)[-4:]}"
        logger.info(f"Выполнено маскирование номера счета {account_number} - результат: {mask_account_number}")
        return mask_account_number
    logger.error(f"Не удалось выполнить маскирование номера счета - передан неверный формат счета: {account_number}")
    raise Exception("Передан неверный формат счета")


# для проверки
# print(masked_card_number(7000792289606361))
# print(masked_account_number(73654108430135874305))
