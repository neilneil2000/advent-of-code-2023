from day18_test_input import day18_input
from lagoon import Lagoon


def main():
    data = parse_input()
    lava_lagoon = Lagoon(data)
    lava_lagoon.dig_perimeter()
    lava_lagoon.dig_internal()
    # lava_lagoon.display()
    # lava_lagoon.flood_fill_outside()
    # lava_lagoon.display()
    # print(f"Part 1: {lava_lagoon.volume}")

    # lava_lagoon.convert_hex_instructions()
    # lava_lagoon.dig_perimeter()
    lava_lagoon.display()
    lava_lagoon.build_vertices()
    lava_lagoon.compute_volume()
    total = 0
    while len(lava_lagoon.path) > 2:
        total += lava_lagoon.volume_of_next_chunk()
        lava_lagoon.display()

    pass


def parse_input():
    parsed = [tuple(row.split(" ")) for row in day18_input.splitlines()]
    return [(row[0], int(row[1]), row[2].strip("()#")) for row in parsed]


if __name__ == "__main__":
    main()
