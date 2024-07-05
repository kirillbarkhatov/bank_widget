from src.masks import masked_account_number, masked_card_number
from src.widget import masked_numbers, convert_date
from src.processing import filter_by_state, sort_by_date, get_count_operations_by_category, search_by_description
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
from src.decorators import log
from src.external_api import currency_converter
from src.utils import get_transactions_from_xls, get_transactions_from_csv, get_transactions_from_json, get_transaction_amount
import json

def greetings() -> list[dict]:
    """Приветствие пользователя, выбор какой файл прочитать"""

    print(
        """
Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями. 
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
        """
    )

    user_choice = input("Пользователь: ")

    match user_choice:
        case "1":
            print("Программа: Для обработки выбран JSON-файл")
            return get_transactions_from_json("data/operations.json")
        case "2":
            print("Программа: Для обработки выбран CSV-файл")
            return get_transactions_from_csv("data/transactions.csv")
        case "3":
            print("Программа: Для обработки выбран XLSX-файл")
            return get_transactions_from_xls("data/transactions_excel.xlsx")
        case _:
            print("\nОШИБКА ВВОДА! Укажите число от 1 до 3")
            return greetings()


def choice_state(operations: list[dict]) -> list[dict]:
    """Выбор статуса операций и фильтрация по нему полученного списка операций"""

    print(
        """
Программа: Введите статус, по которому необходимо выполнить фильтрацию. 
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING
        """
    )

    user_input = input("Пользователь: ").upper()

    if user_input in ["EXECUTED", "CANCELED", "PENDING"]:
        print(f'Программа: Операции отфильтрованы по статусу "{user_input}"\n')
        return filter_by_state(operations, user_input)


    print(f'Программа: Статус операции {user_input} недоступен.')
    return choice_state(operations)


def user_settings(operations: list[dict]) -> list[dict]:
    """Выбор настроек фильтрации"""

    while True:
        print("Программа: Отсортировать операции по дате? Да/Нет")
        user_answer = input("Пользователь: ").lower()
        if user_answer == "да":
            while True:
                print("\nПрограмма: Отсортировать по возрастанию или по убыванию? ")
                user_answer = "по убыванию" #input("Пользователь: ").lower()
                if user_answer == "по возрастанию":
                    operations_processing = sort_by_date(operations, False)
                    break
                elif user_answer == "по убыванию":
                    operations_processing = sort_by_date(operations, True)
                    break
                else:
                    print("\nОшибка ввода - повторите, пожалуйста\n")
            break
        elif user_answer == "нет":
            operations_processing = operations
            break
        else:
            print("\nОшибка ввода - повторите, пожалуйста\n")

    while True:
        print("\nПрограмма: Выводить только рублевые тразакции? Да/Нет ")
        user_answer = input("Пользователь: ").lower()
        if user_answer == "да":
            operations_processing = [tr for tr in filter_by_currency(operations_processing, "RUB")]
            break
        elif user_answer == "нет":
            break
        else:
            print("\nОшибка ввода - повторите, пожалуйста\n")

    while True:
        print("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет ")
        user_answer = input("Пользователь: ").lower()
        if user_answer == "да":
            print("\nПрограмма: введите слово для фильтрации")
            filter_input = input("Пользователь: ")
            operations_processing = search_by_description(operations_processing, filter_input)
            break
        elif user_answer == "нет":
            break
        else:
            print("\nОшибка ввода - повторите, пожалуйста\n")

    return operations_processing


def result_printing(operations: list[dict]) -> None:
    """Вывод результатов"""

    print("Программа: Распечатываю итоговый список транзакций...\n")
    if len(operations) == 0:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Программа: Всего банковских операций в выборке: {len(operations)}")

        for operation in operations:
            print(f'\n{convert_date(operation["date"])} {operation["description"]}')
            if (operation.get('from', 0) == 0) or (operation.get('from', 0) is None) or (operation.get('from', 0) == "NaN"):
                print(masked_numbers(operation["to"]))
            else:
                print(f'{masked_numbers(operation["from"])} -> {masked_numbers(operation["to"])}')

            print(f"Сумма {operation['operationAmount']['amount']} {operation["operationAmount"]["currency"]["code"]}")





if __name__ == '__main__':
    operations_from_file = greetings()
    operations_by_state = choice_state(operations_from_file)
    operations_for_print = user_settings(operations_by_state)
    result_printing(operations_for_print)


# print(f"`{masked_card_number.__name__}`", masked_card_number.__doc__)
# print(f"`{masked_account_number.__name__}`", masked_account_number.__doc__)
# print(f"`{masked_numbers.__name__}`", masked_numbers.__doc__)
# print(f"`{convert_date.__name__}`", convert_date.__doc__)
# print(f"`{filter_by_state.__name__}`", sort_by_date.__doc__)
# print(f"`{filter_by_currency.__name__}`", filter_by_currency.__doc__)
# print(f"`{transaction_descriptions.__name__}`", transaction_descriptions.__doc__)
# print(f"`{card_number_generator.__name__}`", card_number_generator.__doc__)
# print(f"`{log.__name__}`", log.__doc__)
# print(f"`{currency_converter.__name__}`", currency_converter.__doc__)
# print(f"`{get_transactions_from_xls.__name__}`", get_transactions_from_xls.__doc__)
# print(f"`{get_transactions_from_csv.__name__}`", get_transactions_from_csv.__doc__)
# print(f"`{get_transactions_from_json.__name__}`", get_transactions_from_json.__doc__)
# print(f"`{get_transaction_amount.__name__}`", get_transaction_amount.__doc__)


