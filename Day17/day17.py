"""Advent of Code 2023 Day 17"""

from day17_input import day17_input
from ultra_town_map import TownMap


def main():
    """Main Solution"""
    data = parse_input()
    part1_answer = part1(data)
    print(f"Part 1: {part1_answer}")

    part2_answer = part2(data)
    print(f"Part 2: {part2_answer}")


def part1(data):
    """Solution to Part 1"""
    town = TownMap(data)
    town.set_start((0, 0))
    town.set_start_direction(">")
    town.set_target((town.width - 1, town.length - 1))
    return town.get_best_route()


def part2(data):
    """Solution to Part 2"""
    return 0


def parse_input():
    """Return structured representation of input data"""
    structured = []
    for row in day17_input.splitlines():
        new_line = []
        for entry in list(row):
            new_line.append(int(entry))
        structured.append(new_line)
    return structured


if __name__ == "__main__":
    main()
