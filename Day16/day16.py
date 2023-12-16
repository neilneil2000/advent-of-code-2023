import sys
from day16_input import day16_input
from cavernfloor import CavernFloor


def main():
    layout = parse_input()
    cavern = CavernFloor(layout)
    part1_result = cavern.energised_squares()
    print(len(part1_result))


def parse_input():
    return [list(row) for row in day16_input.splitlines()]


if __name__ == "__main__":
    sys.setrecursionlimit = 10000
    main()
