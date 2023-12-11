"""Advent of Code 2023 Day 12"""
from day12_test_input import day12_input


def main():
    """Main Solution"""
    processed = parse_input()

    part1_result = execute_part1(processed)
    print(f"Part 1: {part1_result}")

    part2_result = execute_part2(processed)
    print(f"Part 2: {part2_result}")


def execute_part1(processed):
    """Solution to Part 1"""
    return processed


def execute_part2(processed):
    """Solution to Part 2"""
    return processed


def parse_input():
    """Return Structured Representation of Input"""
    processed = day12_input.splitlines()
    return processed


if __name__ == "__main__":
    main()
