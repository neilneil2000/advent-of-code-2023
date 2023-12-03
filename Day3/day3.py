from typing import List

from schematic import Schematic
from day3_input import day3_input

def main():
    schematic = parse_input()
    elf_map = Schematic(schematic)
    print(elf_map.part_number_total())

def parse_input()->List:
    """Return structured version of input file"""
    return [list(line) for line in day3_input.splitlines()]


if __name__=="__main__":
    main()