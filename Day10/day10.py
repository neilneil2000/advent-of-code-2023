"""Solution to Advent of Code 2023 Day 10"""
from typing import Tuple, List, Set, Dict
from day10_input import day10_input


def main():
    """Solution to Advent of Code 2023 Day 10"""
    metal_map = parse_input()

    distances = part1(metal_map)
    max_distance = max(distances)
    print(f"Part 1: {max_distance}")
    display_pipe_loop(metal_map, distances)
    no_of_enclosed_squares = get_enclosed_squares(metal_map, distances[-1])
    print(f"Part 2: {no_of_enclosed_squares}")


def display_pipe_loop(metal_map, steps):
    """Print Main Pipe Loop"""
    flag = None
    for y, _ in enumerate(metal_map):
        for x, _ in enumerate(metal_map[0]):
            for key, values in steps.items():
                if (x, y) in values:
                    flag = key
            if flag == -1:
                print(".", end="")
            else:
                print(metal_map[y][x], end="")

        print()
    print()


def perimeter_dots(array: List[List[any]]) -> Set:
    """Return set of all dots on perimeter of an array of squares"""
    dots = set()
    row_width = len(array[0])
    column_length = len(array)

    for y, _ in enumerate(array):
        dots.add((0, y))
        dots.add((row_width, y))

    for x, _ in enumerate(array[0]):
        dots.add((x, 0))
        dots.add((x, column_length))

    dots.add((0, column_length))
    dots.add((row_width, column_length))
    dots.add((row_width, 0))

    return dots


def get_enclosed_squares(metal_map, empty_squares):
    """Solution to Part 2"""
    outside_dots = perimeter_dots(metal_map)

    new_dots = outside_dots.copy()
    while new_dots:
        new_dots = get_next_dots(new_dots, metal_map, empty_squares, outside_dots)
        outside_dots.update(new_dots)

    for dot in outside_dots:
        remove_touching_squares(dot, empty_squares)
    return len(empty_squares)


def remove_touching_squares(dot: Tuple[int], squares: Set[Tuple[int]]):
    """If a dot touches a square, remove it from set of squares"""
    x, y = dot
    squares.difference_update({(x, y), (x - 1, y - 1), (x, y - 1), (x - 1, y)})


def get_next_dots(
    starting_dots: Set, metal_map: List, unused_squares: List, outside_dots: Set
):
    """Return all dots connected to starting dots that are not in outside_dots"""
    connected_dots = set()
    for dot in starting_dots:
        connected_dots.update(
            get_connected_dot_neighbours(dot, metal_map, outside_dots, unused_squares)
        )
    return connected_dots


def get_connected_dot_neighbours(
    dot,
    metal_map,
    outside_dots,
    unused_squares,
):
    """Return Set of all valid neighbours to a dot"""
    valid_neighbours = set()
    for neighbour in get_neighbours(dot):
        if is_dot_out_of_bounds(neighbour, metal_map):
            continue
        if neighbour in outside_dots:
            continue
        if are_dots_connected(dot, neighbour, metal_map, unused_squares):
            valid_neighbours.add(neighbour)
    return valid_neighbours


def get_neighbours(location: Tuple[int]) -> Set:
    """Return direction neighbours to a 2D cartesian co-ordinate"""
    x, y = location
    return {(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)}


def are_dots_connected(dot_a, dot_b, pipe_map, unused_squares):
    """Returns True if it's possible to move between dot a to dot b"""
    (a_x, a_y), (b_x, _) = sorted((dot_a, dot_b))
    if a_x == b_x:
        check_values = ["F", "-", "L"]
        transit_squares = [(a_x - 1, a_y), (a_x, a_y)]
    else:
        check_values = ["F", "|", "7"]
        transit_squares = [(a_x, a_y - 1), (a_x, a_y)]

    for square in transit_squares:
        if is_square_out_of_bounds(square, pipe_map) or is_square_unused(
            square, unused_squares
        ):
            return True
    if symbol_at_location(transit_squares[0], pipe_map) in check_values:
        return False
    return True


def symbol_at_location(location, metal_map):
    """Returns symbol at location on map"""
    x, y = location
    if metal_map[y][x] == "S":
        return compute_pipe_shape_at_location(location, metal_map)
    return metal_map[y][x]


def compute_pipe_shape_at_location(location, metal_map):
    """Return shape of pipe that should be at location"""
    x, y = location
    s_options = {"7", "J", "L", "F", "-", "|"}
    if symbol_at_location((x, y - 1), metal_map) in ["F", "|", "7"]:
        s_options.difference_update({"F", "-", "7"})
    if symbol_at_location((x, y + 1), metal_map) in ["J", "|", "L"]:
        s_options.difference_update({"J", "-", "L"})
    if symbol_at_location((x - 1, y), metal_map) in ["F", "-", "L"]:
        s_options.difference_update({"F", "|", "L"})
    if symbol_at_location((x + 1, y), metal_map) in ["J", "-", "7"]:
        s_options.difference_update({"J", "|", "7"})
    return s_options.pop()


def is_square_unused(location, unused_locations):
    """Returns True if location has a pipe that is part of the loop"""
    if location in unused_locations:
        return True
    return False


def is_square_out_of_bounds(square, metal_map):
    """Returns true if location is within scope of map"""
    x, y = square
    if x < 0 or y < 0 or x >= len(metal_map[0]) or y >= len(metal_map):
        return True
    return False


def is_dot_out_of_bounds(dot, metal_map):
    """Returns true if location is within scope of map"""
    x, y = dot
    if x < 0 or y < 0 or x > len(metal_map[0]) or y > len(metal_map):
        return True
    return False


def part1(metal_map):
    "Compute Solution for part 1"
    step_dictionary = {-1: set()}
    for y in range(len(metal_map)):
        for x in range(len(metal_map[0])):
            step_dictionary[-1].add((x, y))
    start = get_start_coordinate(metal_map)
    step_dictionary[-1].remove(start)
    value = 0
    current_squares = {start}
    step_dictionary[value] = current_squares
    while current_squares:
        value += 1
        step_dictionary[value] = set()
        current_squares = calculate_next_step(
            current_squares, step_dictionary, metal_map, value
        )
    if not step_dictionary[value]:
        del step_dictionary[value]
    return step_dictionary


def calculate_next_step(starting_points, steps, m, value):
    """Update dictionary of steps"""
    next_spaces = set()
    for point in starting_points:
        next_spaces.update(pipe_neighbours(point, steps, m, value))
    return next_spaces


def get_valid_neighbours(point: Tuple[int], metal_map: List[List[str]]) -> Tuple:
    """Returns Valid Neighbours for point
    Where you can go from a given square depends on the content of that square
    """
    x, y = point
    up = (x, y - 1)
    down = (x, y + 1)
    left = (x - 1, y)
    right = (x + 1, y)
    symbol = metal_map[y][x]
    if symbol == "S":
        return up, down, left, right
    if symbol == "|":
        return up, down, None, None
    if symbol == "-":
        return None, None, left, right
    if symbol == "L":
        return up, None, None, right
    if symbol == "J":
        return up, None, left, None
    if symbol == "7":
        return None, down, left, None
    if symbol == "F":
        return None, down, None, right
    return None, None, None, None


def pipe_neighbours(point, steps, metal_map, value):
    """Return locations that pipe connects to"""
    valid_characters = (
        ["|", "7", "F"],  # up
        ["|", "L", "J"],  # down
        ["-", "L", "F"],  # left
        ["-", "J", "7"],  # right
    )
    next_spaces = set()

    neighbours = get_valid_neighbours(point, metal_map)
    for neighbour, valid_pipes in zip(neighbours, valid_characters):
        if not is_square_unused(neighbour, steps[-1]):
            continue
        if symbol_at_location(neighbour, metal_map) not in valid_pipes:
            continue
        set_steps_to_pipe_location(neighbour, value, steps)
        next_spaces.add(neighbour)

    return next_spaces


def set_steps_to_pipe_location(location: Tuple[int], steps: int, distances: Dict):
    """Set number of steps to get to a given location"""
    distances[steps].add(location)
    distances[-1].remove(location)


def get_start_coordinate(metal_map: List[List[str]]) -> Tuple:
    """Get location of Start square"""
    for y, row in enumerate(metal_map):
        for x, character in enumerate(row):
            if character == "S":
                return (x, y)
    return (None, None)


def parse_input():
    """Process input to formatted set"""
    metal_map = []
    for line in day10_input.splitlines():
        metal_map.append(list(line))
    return metal_map


if __name__ == "__main__":
    main()
