import json
import logging

from src.external_api import currency_converter

# Настройки логгирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(f"logs/{__name__}.log", mode="w")
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def get_transactions_from_json(file_path: str) -> list[dict]:
    """Функция принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """

    try:
        with open(file_path, "r") as file:
            transactions = json.load(file)
        logger.info(f"Получен список транзакций из файла {file_path}")
        if transactions == "":
            logger.info(f"Файл {file_path} пустой - список транзакций отсутствует")
            return []
        if type(transactions) is not list:
            logger.info(f"В файле {file_path} список транзакций отсутствует")
            return []
        return transactions

    except FileNotFoundError:
        logger.info(f"Файл {file_path} не найден")
        return []


def get_transaction_amount(transaction: dict) -> float:
    """Функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях, тип данных — float.
    Если транзакция была в USD или EUR, происходит обращение к внешнему API для получения текущего курса валют
    и конвертации суммы операции в рубли
    """

    try:
        transaction_amount = float(transaction["operationAmount"]["amount"])
        transaction_currency = transaction["operationAmount"]["currency"]["code"]

        if transaction_currency == "RUB":
            logger.info("Сумма транзакции получена успешно")
            return transaction_amount

        convert_transaction_amount = currency_converter(transaction_amount, transaction_currency)
        logger.info("Сумма транзакции успешно получена и сконвертирована")
        return convert_transaction_amount
    except Exception:
        logger.error("Не удалось обработать транзакцию - проверьте формат данных")
        raise Exception("Не удалось обработать транзакцию - проверьте формат данных")
