import pytest

from day1 import get_first_number, get_last_number

get_first_params = [("one", "1"), ("one2", "1"), ("oneight", "1"), ("seveone", "1")]


@pytest.mark.parametrize("test_input,expected", get_first_params)
def test_get_first_number(test_input, expected):
    """Validate get_first_number is working correctly"""
    assert get_first_number(test_input) == expected


def test_get_last_number():
    """Validate get_last_number is working correctly"""
    assert get_last_number("one") == "1"
    assert get_last_number("one2") == "2"
    assert get_last_number("oneight") == "8"
    assert get_last_number("seveone") == "1"
    assert get_last_number("oneven") == "1"
