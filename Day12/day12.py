"""Advent of Code 2023 Day 12"""
from typing import List, Dict
from time import perf_counter
from functools import lru_cache
from day12_input import day12_input


def main():
    """Main Solution"""
    print(f"{perf_counter()}: Program Started")
    processed = parse_input()
    print(f"{perf_counter()}: Starting Part 1")
    part1_result = execute(processed)
    print(f"Part 1: {part1_result}")
    print(f"{perf_counter()}: Starting Part 2")
    part2_result = execute(processed, expansion=True)
    print(f"Part 2: {part2_result}")
    print(f"{perf_counter()}: Complete")


def execute(dataset, expansion=False):
    """Solution"""
    totals = []
    for springs, lengths in dataset:
        if expansion:
            springs, lengths = unfold(springs, lengths)
        result = count_combinations({springs: 1}, lengths)
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


def count_valid_combos(springs_dict: Dict):
    """Return total number of valid combinations"""
    return sum(count for springs, count in springs_dict.items() if all_dots(springs))


def count_combinations(springs_dict: Dict, lengths: List) -> int:
    """Breadth First Search to return number of valid combinations"""
    if not lengths:
        return count_valid_combos(springs_dict)

    total = 0
    length = lengths[0]
    new_springs = {}

    for springs, count in springs_dict.items():
        for start_point in get_all_start_points(springs, length):
            subsprings = springs[start_point + length + 1 :]
            new_springs[subsprings] = new_springs.get(subsprings, 0) + count

    if new_springs:
        total += count_combinations(new_springs, lengths[1:])

    return total


@lru_cache(maxsize=None)
def all_dots(springs: str):
    """Returns true if it's possible for this row of springs to be all dots"""
    return "#" not in springs


@lru_cache(maxsize=None)
def get_all_start_points(springs: str, length: int) -> List[int]:
    """Return a list of all the points where a contiguous block of springs could exist"""
    start_points = []
    pointer = 0
    while 0 <= pointer < len(springs) - length + 1:
        if "." in springs[pointer : pointer + length]:
            if springs[pointer] == "#":
                pointer = get_next_delimiter(springs, pointer) + 1
                break  # blocked by a dot
            pointer = get_next_delimiter(springs, pointer) + 1
            continue
        if len(springs) == pointer + length or springs[pointer + length] in ["?", "."]:
            start_points.append(pointer)  # terminated by dot or EOL
        if springs[pointer] == "#":
            break
        pointer = get_next_delimiter(springs, pointer) + 1
    return start_points


def get_next_delimiter(springs, pointer):
    """Return location of next delimiter"""
    next_dot = springs.find(".", pointer)
    next_q = springs.find("?", pointer)
    if next_dot >= 0:
        if next_q >= 0:
            return min(next_dot, next_q)
        return next_dot
    if next_q >= 0:
        return next_q
    return -99999


def parse_input():
    """Return Structured Representation of Input"""
    lines = [line.split() for line in day12_input.splitlines()]
    return [(springs, list(map(int, lengths.split(",")))) for springs, lengths in lines]


if __name__ == "__main__":
    main()
