"""Advent of Code 2023 Day 16"""
from cavernfloor import CavernFloor
from day16_input import day16_input

from time import perf_counter


def main():
    """Main Solution"""
    layout = parse_input()
    cavern = CavernFloor(layout)
    a = perf_counter()
    part1_result = cavern.energised_squares()
    b = perf_counter()
    print(b - a, part1_result)
    part2_result = cavern.most_energised_squares()
    c = perf_counter()
    print(c - b, part2_result)


def parse_input():
    """Return Structured representation of input data"""
    return [list(row) for row in day16_input.splitlines()]


if __name__ == "__main__":
    main()
