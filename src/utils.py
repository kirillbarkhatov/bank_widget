import json

from src.external_api import currency_converter


def get_transactions_from_json(file_path: str) -> list[dict]:
    """Функция принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """

    try:
        with open(file_path, "r") as file:
            transactions = json.load(file)
        if transactions == "":
            return []
        if type(transactions) is not list:
            return []
        return transactions

    except FileNotFoundError:
        return []


def get_transaction_amount(transaction: dict) -> float:
    """Функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях, тип данных — float.
    Если транзакция была в USD или EUR, происходит обращение к внешнему API для получения текущего курса валют
    и конвертации суммы операции в рубли
    """

    transaction_amount = float(transaction["operationAmount"]["amount"])
    transaction_currency = transaction["operationAmount"]["currency"]["code"]

    if transaction_currency == "RUB":
        return transaction_amount

    return currency_converter(transaction_amount, transaction_currency)
