from day2 import compute_minimum_set


def test_compute_minimum_set():
    assert compute_minimum_set(
        [{"blue": 3, "red": 4}, {"red": 1, "green": 2, "blue": 6}, {"green": 2}]
    ) == {"red": 4, "green": 2, "blue": 6}
