from day5 import split_range_a_by_range_b


def test_split_range_a_by_range_b():
    range_1 = (2, 5)  #   2--5
    range_2 = (7, 8)  #        78
    range_3 = (5, 6)  #      56
    range_4 = (4, 6)  #     4-6
    range_5 = (4, 5)  #     45
    range_6 = (3, 4)  #    34
    range_7 = (2, 3)  #   23
    range_8 = (1, 2)  #  12
    range_9 = (0, 1)  # 01
    assert split_range_a_by_range_b(range_1, range_2) == ((), [(2, 5)])
    assert split_range_a_by_range_b(range_1, range_3) == ((5, 5), [(2, 4)])
    assert split_range_a_by_range_b(range_1, range_4) == ((4, 5), [(2, 3)])
    assert split_range_a_by_range_b(range_1, range_5) == ((4, 5), [(2, 3)])
    assert split_range_a_by_range_b(range_1, range_6) == ((3, 4), [(2, 2), (5, 5)])
    assert split_range_a_by_range_b(range_1, range_7) == ((2, 3), [(4, 5)])
    assert split_range_a_by_range_b(range_1, range_8) == ((2, 2), [(3, 5)])
    assert split_range_a_by_range_b(range_1, range_9) == ((), [(2, 5)])
    assert split_range_a_by_range_b(range_6, range_1) == ((3, 4), [])
