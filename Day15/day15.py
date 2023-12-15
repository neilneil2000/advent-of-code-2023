"""Advent of Code 2023 Day 15"""
from day15_input import day15_input
from hashmap import Hashmap


def main():
    """Main Function"""
    instructions = day15_input.split(",")
    part1_result = part1(instructions)
    print(part1_result)
    part2_result = part2(instructions)
    print(part2_result)


def part1(instructions):
    """Find solution to part 1"""
    return sum(Hashmap.hasher(c) for c in instructions)


def part2(instructions):
    """Find solution to part 2"""
    hashmap = Hashmap()
    for i in instructions:
        if "=" in i:
            label, focal = i.split("=")
            hashmap.set(label, int(focal))
            continue
        label = i[:-1]
        hashmap.remove(label)
    return hashmap.score


if __name__ == "__main__":
    main()
