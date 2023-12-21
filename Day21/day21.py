from day21_test_input import day21_input
from garden import Garden


def main():
    garden = Garden(parse_input())
    part1_result = garden.locations_after_steps(500, True)
    print(f"Part 1: {part1_result}")


def parse_input():
    """Return structured representation of input"""
    return [list(row) for row in day21_input.splitlines()]


if __name__ == "__main__":
    main()
