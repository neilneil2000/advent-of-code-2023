from day18_input import day18_input
from lagoon import Lagoon


def main():
    data = parse_input()
    lava_lagoon = Lagoon(data)
    lava_lagoon.dig_perimeter()
    lava_lagoon.dig_internal()
    lava_lagoon.display()
    lava_lagoon.flood_fill_outside()
    lava_lagoon.display()
    print(lava_lagoon.volume)


def parse_input():
    parsed = [tuple(row.split(" ")) for row in day18_input.splitlines()]
    return [(row[0], int(row[1]), int(row[2].strip("()#"), 16)) for row in parsed]


if __name__ == "__main__":
    main()
