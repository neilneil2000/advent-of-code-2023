"""Advent of Code 2023 Day 15"""
from day15_input import day15_input
from hashmap import Hashmap


def main():
    """Main Function"""
    instructions = day15_input.split(",")
    part1_result = part1(instructions)
    print(part1_result)


def part1(instructions):
    """Find solution to part 1"""
    return sum(Hashmap.hasher(c) for c in instructions)


if __name__ == "__main__":
    main()
