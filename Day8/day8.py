import math

from day8_input import day8_input


def main():
    directions, nodes = parse_input()
    steps = steps_from_a_to_z(directions, nodes)
    print(f"Part 1: {steps}")
    steps = steps_from_a_to_z_part_2(directions, nodes)
    print(f"Part 2: {steps}")


def steps_from_a_to_z(directions, nodes):
    """Part 1 Implementation"""
    position = "AAA"
    pointer = 0
    while position != "ZZZ":
        position = nodes[position][int(directions[pointer % len(directions)])]
        pointer += 1
    return pointer


def get_starting_positions(nodes):
    """Return list of starting positions"""
    return [node for node in nodes if node[-1] == "A"]


def steps_from_a_to_z_part_2(directions, nodes):
    """Part2 Implementation"""
    positions = get_starting_positions(nodes)
    end_points = []
    for position in positions:
        pointer = 0
        while position[-1] != "Z":
            position = nodes[position][int(directions[pointer % len(directions)])]
            pointer += 1
        end_points.append(pointer)
    return math.lcm(*end_points)


def parse_input():
    directions, raw_nodes = day8_input.split("\n\n")
    directions = directions.replace("L", "0")
    directions = directions.replace("R", "1")

    nodes = {}
    for raw_node in raw_nodes.splitlines():
        origin, destinations = raw_node.split("=")
        destinations = destinations.strip()[1:-1]
        left, right = destinations.split(",")
        nodes[origin.strip()] = (left.strip(), right.strip())
    return directions, nodes


if __name__ == "__main__":
    main()
