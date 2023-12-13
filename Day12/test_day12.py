from day12 import (
    is_valid_combination,
    good_so_far,
    has_potential,
    count_combinations,
    get_all_start_points,
)


def test_is_valid_combination():
    assert not is_valid_combination("???.###", [1, 1, 3])
    assert not is_valid_combination("#.#.###", [1, 2, 3])
    assert is_valid_combination("#.#.###", [1, 1, 3])


def test_good_so_far():
    assert good_so_far("?.#.#?#", [1, 1, 3])
    assert good_so_far("?.?.###", [1, 1, 3])
    assert good_so_far("???.###", [1, 1, 3])
    assert good_so_far("?.#.###", [1, 1, 3])
    assert good_so_far("???????", [1, 1, 3])
    assert good_so_far("?.??.##", [2, 2])
    assert not good_so_far("....####", [1, 1, 3])


def test_has_potential():
    assert has_potential("?.#.#?#", [1, 1, 3])
    assert has_potential("?.?.###", [1, 1, 3])
    assert has_potential("???.###", [1, 1, 3])
    assert has_potential("?.#.###", [1, 1, 3])
    assert has_potential("???????", [1, 1, 3])
    assert not has_potential("?.??.##", [2, 2])
    assert not has_potential("....####", [1, 1, 3])
    assert has_potential("???.????", [1, 4])
    assert has_potential("?##?..??", [4, 2])
    assert has_potential("?##?..??", [4, 1])
    assert has_potential(".??..??...?##.", [1, 1, 3])
    assert has_potential("?.#.#?#", [1, 3])


def test_count_combinations():
    assert count_combinations("?.???.?#?###?", [1, 1, 1, 3]) == (4, False)
    assert count_combinations("#??.#.??????##?", [1, 1, 7]) == (2, False)
    assert count_combinations("?????...#??", [5, 1]) == (1, False)
    assert count_combinations("?.#.#?#", [1, 3]) == (2, False)
    assert count_combinations(".??..??...?##.", [1, 1, 3]) == (4, False)
    # assert (
    #    count_combinations(
    #        "?###??????????###??????????###??????????###??????????###????????",
    #        [3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1],
    #    )
    #    == (506250, False)
    # )


def test_get_all_start_points():
    assert get_all_start_points("?.#.#?#", 1) == [0, 2, 4, 6]
    assert get_all_start_points("?.#.#?#", 2) == []
    assert get_all_start_points("?.#.#?#", 3) == [4]
    assert get_all_start_points("?.#.#?#", 4) == []
    assert get_all_start_points("?.#.#?#", 5) == []
    assert get_all_start_points("?.#.#?#", 6) == []
    assert get_all_start_points("?#?#?#?", 2) == [0, 5]
    assert get_all_start_points("..#??", 1) == [2]
