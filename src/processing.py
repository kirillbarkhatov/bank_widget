import re


def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция принимает на вход список словарей и значение для ключа
    state (опциональный параметр со значением по умолчанию EXECUTED)
    и возвращает новый список, содержащий только те словари,
    у которых ключ state содержит переданное в функцию значение
    """

    return [operation for operation in operations if operation["state"] == state]


def sort_by_date(operations: list[dict], is_reverse: bool = True) -> list[dict]:
    """Функция принимает на вход список словарей и возвращает новый список,
    в котором исходные словари отсортированы по убыванию даты (ключ date).
    Функция принимает два аргумента, второй необязательный задает
    порядок сортировки (убывание, возрастание)
    """

    return [operation for operation in sorted(operations, key=lambda x: x["date"], reverse=is_reverse)]


def search_by_description(operations: list[dict], user_search: str) -> list[dict]:
    """Функция принимает список словарей с данными о банковских операциях и строку поиска
    и возвращает список словарей, у которых в описании есть данная строка
    """

    return [operation for operation in operations if re.search(user_search, operation["description"])]


# тестирование
if __name__ in "__main__":
    test_data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364', 'description': 'Перевод между счетами'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572', 'description': 'Перевод по СБП'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689', 'description': 'Зачисление на счет'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441', 'description': 'Зачисление по СБП'}
    ]
    print(filter_by_state(test_data, 'CANCELED'))
    print(sort_by_date(test_data, True))
    print(search_by_description(test_data, 'Перевод'))
