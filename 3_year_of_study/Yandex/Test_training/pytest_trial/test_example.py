# test_example.py
import pytest


def one_more(x):
    return x + 1


@pytest.mark.parametrize(
    'input_arg, expected_result',
    [(4, 5), (3, 5)],
    ids=['First parameter', 'Second parameter',]
)
def test_one_more(input_arg, expected_result):
    assert one_more(input_arg) == expected_result


def get_sort_list(str):
    new_list = sorted(str.split(', '))
    return new_list


def test_sort():
    """Тестируем функцию get_sort_list()."""
    result = get_sort_list('Яша, Саша, Маша, Даша')
    assert result == ['Даша', 'Маша', 'Саша', 'Яша']


def test_type():
    """Тестируем тип данных, возвращаемых из get_sort_list()."""
    # Провальный тест:
    # ожидаем число, но вернётся список.
    result = get_sort_list('Яша, Саша, Маша, Даша')
    assert isinstance(result, int)
