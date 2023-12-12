"""Advent of Code 2023 Day 12"""
from typing import List
from day12_input import day12_input


def main():
    """Main Solution"""
    processed = parse_input()

    part1_result = execute_part1(processed)
    print(f"Part 1: {part1_result}")

    # part2_result = execute_part2(processed)
    # print(f"Part 2: {part2_result}")


def execute_part1(dataset):
    """Solution to Part 1"""
    totals = []
    for springs, lengths in dataset:
        totals.append(valid_combinations(springs, lengths))
    print(totals)
    return sum(totals)


def valid_combinations(springs: str, lengths: List) -> int:
    """Return number of possible combinations possible for given spring row"""
    if (index := springs.find("?")) < 0:
        return 1 if is_valid_combination(springs, lengths) else 0
    total = 0
    total += valid_combinations(springs[:index] + "." + springs[index + 1 :], lengths)
    total += valid_combinations(springs[:index] + "#" + springs[index + 1 :], lengths)
    return total


def is_valid_combination(springs: str, lengths: List) -> bool:
    """Return True if spring combination is valid"""
    if not set(springs) == {".", "#"}:
        return False
    return lengths == [len(entry) for entry in springs.split(".") if entry]


def execute_part2(processed):
    """Solution to Part 2"""
    return processed


def parse_input():
    """Return Structured Representation of Input"""
    lines = [line.split() for line in day12_input.splitlines()]
    parsed = []
    for springs, lengths in lines:
        parsed.append((springs, list(map(int, lengths.split(",")))))
    return parsed


if __name__ == "__main__":
    main()
