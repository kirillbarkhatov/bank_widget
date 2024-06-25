import json


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
