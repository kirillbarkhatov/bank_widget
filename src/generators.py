from typing import Generator


def filter_by_currency(transactions: list[dict], currency: str) -> Generator[dict, None, None]:
    """Функция - генератор принимает список словарей с банковскими операциями
    (или объект-генератор, который выдает по одной банковской операции)
    и возвращает итератор, который выдает по очереди операции, в которых указана заданная валюта
    """
    filtered_transactions = (
        transaction for transaction in transactions if transaction["operationAmount"]["currency"]["code"] == currency
    )
    for filtered_transaction in filtered_transactions:
        yield filtered_transaction


def transaction_descriptions(transactions: list[dict]) -> Generator[str, None, None]:
    """Функция - генератор, который принимает список словарей
    и возвращает описание каждой операции по очереди
    """

    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """Генератор номеров банковских карты - диапазоны передаются как параметры генератора"""
    card_number = start
    while card_number <= end:
        length = len(str(card_number))
        full_card_number = "0" * (16 - length) + str(card_number)
        yield f"{full_card_number[:4]} {full_card_number[4:8]} {full_card_number[8:12]} {full_card_number[12:]}"
        card_number += 1
