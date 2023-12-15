"""Advent of Code 2023 Day 15"""
from day15_input import day15_input


def main():
    """Main Function"""
    instructions = day15_input.split(",")
    part1_result = part1(instructions)
    print(part1_result)


def part1(instructions):
    """Find solution to part 1"""
    return sum(hasher(c) for c in instructions)


def hasher(instruction: str) -> int:
    """Compute hash on string"""
    current_value = 0
    for character in instruction:
        current_value += ord(character)
        current_value *= 17
        current_value %= 256
    return current_value


if __name__ == "__main__":
    main()
