import pytest

from src.processing import filter_by_state, sort_by_date, search_by_description, get_count_operations_by_category


@pytest.fixture
def operations():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture()
def operations_2():
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364', 'description': 'Перевод между счетами'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572', 'description': 'Перевод по СБП'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689', 'description': 'Зачисление на счет'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689',
         'description': 'Зачисление на счет'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441', 'description': 'Зачисление по СБП'}
    ]


@pytest.mark.parametrize(
    "state, filtered_data",
    [
        (
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
    ],
)
def test_filter_by_state(operations, state, filtered_data):
    assert filter_by_state(operations, state) == filtered_data


@pytest.mark.parametrize(
    "is_reverse, sorted_data",
    [
        (
            False,
            [
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            ],
        ),
        (
            True,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
    ],
)
def test_sort_by_date(operations, is_reverse, sorted_data):
    assert sort_by_date(operations, is_reverse) == sorted_data

@pytest.mark.parametrize(
    "user_search, output_data",
    [
        (
            "Перевод",
            [
                {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364', 'description': 'Перевод между счетами'},
                {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572', 'description': 'Перевод по СБП'}
            ]
        ),
        (
            "СБП",
            [
                {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572', 'description': 'Перевод по СБП'},
                {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441', 'description': 'Зачисление по СБП'}
            ]
        ),
        (
            "Зачисление",
            [
                {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689',
                 'description': 'Зачисление на счет'},
                {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689',
                 'description': 'Зачисление на счет'},
                {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441',
                 'description': 'Зачисление по СБП'}
            ]
        )
    ]
)
def test_search_by_description(operations_2, user_search, output_data):
    assert search_by_description(operations_2, user_search) ==output_data


def test_get_count_operations_by_category(operations_2):
    user_list = ['Перевод между счетами', 'Перевод по СБП', 'Зачисление на счет', 'Зачисление по СБП']
    output_data = {'Перевод между счетами': 1, 'Перевод по СБП': 1, 'Зачисление на счет': 2, 'Зачисление по СБП': 1}
    assert get_count_operations_by_category(operations_2, user_list) == output_data
