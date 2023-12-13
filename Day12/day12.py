"""Advent of Code 2023 Day 12"""
from typing import List, Dict
from datetime import datetime
from functools import lru_cache
from day12_input import day12_input


def main():
    """Main Solution"""
    processed = parse_input()

    part1_result = execute(processed)
    print(f"Part 1: {part1_result}")

    part2_result = execute(processed, expansion=True)
    print(f"Part 2: {part2_result}")


def execute(dataset, expansion=False):
    """Solution"""
    totals = []
    for springs, lengths in dataset:
        if expansion:
            springs, lengths = unfold(springs, lengths)
        result = count_combinations_breadth({springs: 1}, lengths)
        print(datetime.now(), springs, lengths, result)
        totals.append(result)
    return sum(totals)


def unfold(springs: str, lengths: List):
    """Unfold inputs to 5 times"""
    unfolded_s = springs
    unfolded_l = lengths.copy()
    for _ in range(4):
        unfolded_s += "?" + springs
        unfolded_l.extend(lengths)

    return unfolded_s, unfolded_l


def valid_combinations(springs: str, lengths: List) -> int:
    """Return number of possible combinations possible for given spring row"""
    if "?" not in springs:
        return 1 if is_valid_combination(springs, lengths) else 0
    # if no_hoper(springs, lengths):
    #    return 0
    index = springs.find("?")

    return valid_combinations(
        springs[:index] + "." + springs[index + 1 :], lengths
    ) + valid_combinations(springs[:index] + "#" + springs[index + 1 :], lengths)


def count_combinations_breadth(springs_dict: Dict, lengths: List) -> int:
    """Breadth First Search to return number of valid combinations"""
    total = 0
    lengths_copy = lengths.copy()
    if lengths_copy:
        length = lengths_copy.pop(0)
    else:
        length = 0
    new_springs = {}
    # if lengths is empty confirm remainder can be all dots
    for springs, count in springs_dict.items():
        if length == 0 and all_dots(springs):
            total += count
            continue

        start_points = get_all_start_points(springs, length)

        for start_point in start_points:
            subsprings = springs[start_point + length + 1 :]
            new_springs[subsprings] = new_springs.get(subsprings, 0) + count
    if new_springs:
        total += count_combinations_breadth(new_springs, lengths_copy)

    return total


def count_combinations(springs: str, lengths: List) -> int:
    # if lengths is empty confirm remainder can be all dots
    if not lengths:
        return (1, False) if all_dots(springs) else (0, False)
    if not springs:
        return 0, True  # No point continuing if no springs left
    # get all start points for first length in list
    lengths_copy = lengths.copy()
    this_block = lengths_copy.pop(0)
    start_points = get_all_start_points(springs, this_block)
    total = 0
    for start_point in start_points:
        count, pointless = count_combinations(
            springs[start_point + this_block + 1 :], lengths_copy
        )
        total += count
        if pointless:
            break

    return total, False


def all_dots(springs: str):
    """Returns true if it's possible for this row of springs to be all dots"""
    return "#" not in springs


def get_all_start_points(springs: str, block_length: int) -> List[int]:
    """Return a list of all the points where a contiguous block of springs could exist"""
    start_points = []
    pointer = 0
    while 0 <= pointer < len(springs) - block_length + 1:
        if "." in springs[pointer : pointer + block_length]:
            if springs[pointer] == "#":
                pointer = get_next_delimiter(springs, pointer) + 1
                break  # blocked by a dot
            else:
                pointer = get_next_delimiter(springs, pointer) + 1
                continue
        if pointer + block_length == len(springs) or springs[
            pointer + block_length
        ] in ["?", "."]:
            start_points.append(pointer)  # terminated by dot or EOL
        if springs[pointer] == "#":
            break
        pointer = get_next_delimiter(springs, pointer) + 1
    return start_points


@lru_cache(maxsize=None)
def get_all_start_points_old(springs: str, block_length: int) -> List[int]:
    """Return a list of all the points where a contiguous block of springs could exist"""
    start_points = []
    pointer = 0
    while 0 <= pointer < len(springs) - block_length + 1:
        if "." in springs[pointer : pointer + block_length]:
            pointer = get_next_delimiter(springs, pointer) + 1
            continue  # blocked by a dot
        if pointer + block_length == len(springs) or springs[
            pointer + block_length
        ] in ["?", "."]:
            start_points.append(pointer)  # terminated by dot or EOL
        pointer = get_next_delimiter(springs, pointer) + 1
    return start_points


def get_next_delimiter(springs, pointer):
    next_dot = springs.find(".", pointer)
    next_q = springs.find("?", pointer)
    if next_dot >= 0:
        if next_q >= 0:
            return min(next_dot, next_q)
        return next_dot
    if next_q >= 0:
        return next_q
    return -99999


def valid_combinations_2(springs: str, lengths: List) -> int:
    # Is this even theoretically possible?
    if (
        len(springs) < sum(lengths) + len(lengths) - 1
    ):  # Is springs long enough to encompass all lengths?
        return 0
    if springs.count("#") > sum(lengths):  # are there more # in springs that needed
        return 0

    target = lengths.pop(0)
    if (next_dot := springs.find(".")) < 0:
        return 0
    while next_dot < target:
        next_dot = springs[next_dot + 1 :].find(".")
        if next_dot < 0:
            return 0
    valid_combinations_2(springs[target:], lengths)


def no_hoper(springs: str, lengths: List) -> bool:
    """
    Returns True if result not possible
    Note: this only returns yes if it's obvious it's a no hoper. It might still resolve to 0
    """
    globs = [len(glob) for glob in springs.split(".")]
    if sum(globs) < sum(lengths):
        return True
    max_length = max(lengths)
    if max_length > max(globs):
        return True
    if len([glob for glob in globs if glob >= max_length]) < lengths.count(max_length):
        return True
    """ slice_springs = springs[: springs.find("?")]
    slice_springs = slice_springs.split(".")
    slice_springs = [len(item) for item in slice_springs if item]
    for index, entry in enumerate(slice_springs):
        if index >= len(lengths):
            break
        if lengths[index] == entry:
            continue
        if index == len(slice_springs) - 1:
            if lengths[index] < entry:
                return True
        else:
            return False """
    return False


def has_potential(springs: str, lengths: List) -> bool:
    """Returns True if this the current string list can match the lengths list"""
    remaining_lengths = lengths.copy()
    target_length = remaining_lengths.pop(0)
    questions = 0
    hashes = 0
    for index, character in enumerate(springs):
        if character == "?":
            if questions + hashes == target_length:
                questions = 0
                hashes = 0
                if remaining_lengths:
                    target_length = remaining_lengths.pop(0)
                else:
                    return "#" not in springs[index:]
            else:
                questions += 1
        elif character == ".":
            if hashes > 0:
                if questions + hashes != target_length:
                    return False
            elif remaining_lengths:
                target_length = remaining_lengths.pop(0)
            else:
                return "#" not in springs[index:]
            questions = 0
            hashes = 0

        elif character == "#":
            hashes += 1

    return questions + hashes == target_length


def good_so_far(springs: str, lengths: List) -> bool:
    """Return True if solution can still potentially be found on this path"""
    confirmed_lengths = []
    current_length = 0
    for character in springs:
        if character == "?":
            break
        if character == "." and current_length > 0:
            confirmed_lengths.append(current_length)
            current_length = 0
        if character == "#":
            current_length += 1

    return confirmed_lengths == lengths[: len(confirmed_lengths)]


def calc_lengths(springs: str):
    """Returns list of lengths of contiguous # for givens springs"""
    return [len(entry) for entry in springs.split(".") if entry]


def is_valid_combination(springs: str, lengths: List) -> bool:
    """Return True if spring combination is valid"""
    if not set(springs) == {".", "#"}:
        return False
    return lengths == calc_lengths(springs)


def parse_input():
    """Return Structured Representation of Input"""
    lines = [line.split() for line in day12_input.splitlines()]
    parsed = []
    for springs, lengths in lines:
        parsed.append((springs, list(map(int, lengths.split(",")))))
    return parsed


if __name__ == "__main__":
    main()
