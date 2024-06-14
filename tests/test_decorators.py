import pytest
from src.decorators import log


def test_log_in_console_decorator(capsys):
    @log()
    def my_function(x, y):
        return x + y
    my_function(1, 2)
    captured = capsys.readouterr()
    assert captured.out == "my_function ok\n"

    with pytest.raises(Exception):
        my_function(1, "2")
    captured = capsys.readouterr()
    assert captured.out == "my_function error: TypeError (unsupported operand type(s) for +: 'int' and 'str'). Inputs: (1, '2'), {}\n"



def test_log_in_file_decorator():
    filename = "test_mylog.txt"
    @log(filename)
    def my_function(x, y):
        return x + y
    my_function(1, 2)
    with open(filename, "r") as f:
        last_log = f.readlines()[-1]
    assert last_log == "my_function ok"

    with pytest.raises(Exception):
        my_function(1, "2")
    with open(filename, "r") as f:
        last_log = f.readlines()[-1]
    assert last_log == "my_function error: TypeError (unsupported operand type(s) for +: 'int' and 'str'). Inputs: (1, '2'), {}"



