from typing import List

from schematic import Schematic
from day3_input import day3_input


def main():
    schematic = parse_input()
    gondola_engine_diagram = Schematic(schematic)
    print(f"Part1: {gondola_engine_diagram.part_number_total()}")
    print(f"Part2: {gondola_engine_diagram.gear_ratio_total()}")


def parse_input() -> List:
    """Return structured version of input file"""
    return [list(line) for line in day3_input.splitlines()]


if __name__ == "__main__":
    main()
