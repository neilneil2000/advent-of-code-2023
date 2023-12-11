from typing import List, Tuple

from day11_input import day11_input


def main():
    universe = parse_input()
    result = part1(universe)
    print(f"Part 1 Result is: {result}")


def part1(universe):
    """Computer answer to part1"""
    display_universe(universe)
    rows, columns = expand_universe(universe)

    galaxies = get_galaxy_locations(universe)

    distances = []
    for index, galaxy_a in enumerate(galaxies):
        for galaxy_b in galaxies[index + 1 :]:
            distances.append(
                get_distance_between_galaxies(galaxy_a, galaxy_b, rows, columns)
            )

    return sum(distances)


def get_distance_between_galaxies(galaxy_a, galaxy_b, rows, columns):
    """Return Distance between galaxies (Expanded Manhattan)"""
    a_x, a_y = galaxy_a
    b_x, b_y = galaxy_b
    multiplier = 1_000_000 - 1
    return (
        abs(a_x - b_x)
        + abs(a_y - b_y)
        + (get_entries_in_range(a_x, b_x, columns) * multiplier)
        + (get_entries_in_range(a_y, b_y, rows) * multiplier)
    )


def get_entries_in_range(start, finish, entries):
    """Returns number of entries between start and finish"""
    if start > finish:
        finish, start = start, finish
    counter = 0
    for entry in entries:
        if start < entry < finish:
            counter += 1
    return counter


def get_galaxy_locations(universe: List[List[str]]) -> List[Tuple[int]]:
    galaxies = []
    for y, row in enumerate(universe):
        for x, value in enumerate(row):
            if value == "#":
                galaxies.append((x, y))
    return galaxies


def display_universe(universe):
    """Print Universe to Screen"""
    for row in universe:
        print("".join(row))
    print()


def get_expanded_rows(universe):
    """Returns list of row indices that need expansion"""
    empty_rows = []
    for index, row in enumerate(universe):
        if set(row) == {"."}:
            empty_rows.append(index)
    return empty_rows


def get_expanded_columns(universe):
    """Returns list of column indices that need expansion"""
    universe_tr = list(map(list, zip(*universe)))
    return get_expanded_rows(universe_tr)


def expand_universe(universe: List):
    return get_expanded_rows(universe), get_expanded_columns(universe)


def expand_universe_old(universe: List) -> None:
    """Expand blank rows in both directions"""
    universe = expand_universe_1d(universe)
    universe = list(map(list, zip(*universe)))
    universe = expand_universe_1d(universe)
    universe = list(map(list, zip(*universe)))

    return universe


def expand_universe_1d(universe: List) -> None:
    """Expand blank rows in 1 dimension"""
    empty_rows = []
    for index, row in enumerate(universe):
        if set(row) == {"."}:
            empty_rows.append(index)
    row_of_dots = ["." for _ in range(len(universe[0]))]
    for index, row_number in enumerate(empty_rows):
        universe.insert(index + row_number, row_of_dots)

    return universe


def parse_input():
    return [list(line) for line in day11_input.splitlines()]


if __name__ == "__main__":
    main()
