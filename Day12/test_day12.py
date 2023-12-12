from day12 import is_valid_combination


def test_is_valid_combination():
    assert not is_valid_combination("???.###", [1, 1, 3])
    assert not is_valid_combination("#.#.###", [1, 2, 3])
    assert is_valid_combination("#.#.###", [1, 1, 3])
