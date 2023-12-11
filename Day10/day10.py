"""Solution to Advent of Code 2023 Day 10"""
from typing import Tuple, List, Set
from day10_input import day10_input


def main():
    """Solution to Advent of Code 2023 Day 10"""
    metal_map = parse_input()

    distance_dictionary = part1(metal_map)
    max_distance = max(distance_dictionary)
    print(f"Part 1: {max_distance}")

    no_of_enclosed_squares = get_enclosed_squares(metal_map, distance_dictionary[-1])
    print(f"Part 2: {no_of_enclosed_squares}")


def display_pipe_loop(metal_map, steps):
    """Print Main Pipe Loop"""

    for y, _ in enumerate(metal_map):
        for x, _ in enumerate(metal_map[0]):
            for key, values in steps.items():
                if (x, y) in values:
                    break
            if key == -1:
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
    new_outside_dots = set()
    for x, y in starting_dots:
        if y > 0 and (x, y - 1) not in outside_dots:  # up
            if are_dots_connected((x, y), (x, y - 1), metal_map, unused_squares):
                new_outside_dots.add((x, y - 1))

        if x < len(metal_map[0]) - 1 and (x + 1, y) not in outside_dots:  # right
            if are_dots_connected((x, y), (x + 1, y), metal_map, unused_squares):
                new_outside_dots.add((x + 1, y))

        if y < len(metal_map) - 1 and (x, y + 1) not in outside_dots:  # down
            if are_dots_connected((x, y), (x, y + 1), metal_map, unused_squares):
                new_outside_dots.add((x, y + 1))

        if x > 0 and (x - 1, y) not in outside_dots:  # left
            if are_dots_connected((x, y), (x - 1, y), metal_map, unused_squares):
                new_outside_dots.add((x - 1, y))

    return new_outside_dots


def are_dots_connected(dot_a, dot_b, pipe_map, unused_squares):
    """Returns true if it's possible to move from dot a to dot b"""
    (a_x, a_y), (b_x, _) = sorted((dot_a, dot_b))
    if a_x == b_x:
        check_values = ["F", "-", "L"]
        transit_squares = [(a_x - 1, a_y), (a_x, a_y)]
    else:
        check_values = ["F", "|", "7"]
        transit_squares = [(a_x, a_y - 1), (a_x, a_y)]

    for square in transit_squares:
        if is_location_out_of_bounds(square, pipe_map) or is_location_unused(
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


def is_location_unused(location, unused_locations):
    """Returns True if location has a pipe that is part of the loop"""
    if location in unused_locations:
        return True
    return False


def is_location_out_of_bounds(location, metal_map):
    """Returns true if location is within scope of map"""
    x, y = location
    if x < 0 or y < 0 or x >= len(metal_map[0]) or y >= len(metal_map):
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
        next_spaces.update(update_neighbours(point, steps, m, value))
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


def update_neighbours(point, steps, m, value):
    up_valid = ["|", "7", "F"]
    down_valid = ["|", "L", "J"]
    left_valid = ["-", "L", "F"]
    right_valid = ["-", "J", "7"]
    up, down, left, right = get_valid_neighbours(point, m)
    next_spaces = set()
    # print(m[up[1]][up[0]])
    if up in steps[-1] and m[up[1]][up[0]] in up_valid:
        steps[value].add(up)
        steps[-1].remove(up)
        next_spaces.add(up)

    if down in steps[-1] and m[down[1]][down[0]] in down_valid:
        steps[value].add(down)
        steps[-1].remove(down)
        next_spaces.add(down)

    if left in steps[-1] and m[left[1]][left[0]] in left_valid:
        steps[value].add(left)
        steps[-1].remove(left)
        next_spaces.add(left)

    if right in steps[-1] and m[right[1]][right[0]] in right_valid:
        steps[value].add(right)
        steps[-1].remove(right)
        next_spaces.add(right)

    return next_spaces


def get_start_coordinate(m):
    """Get location of Start square"""
    for y in range(len(m)):
        for x in range(len(m[y])):
            if m[y][x] == "S":
                return (x, y)


def parse_input():
    metal_map = []
    for line in day10_input.splitlines():
        metal_map.append(list(line))
    return metal_map


if __name__ == "__main__":
    main()
