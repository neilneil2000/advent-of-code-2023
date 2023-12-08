import math

from day8_input import day8_input

# day8_input = day8_input2


def main():
    directions, nodes = parse_input()
    steps = steps_from_a_to_z(directions, nodes)
    print(steps)
    steps = steps_from_a_to_z_modulo(directions, nodes)
    print(steps)


def steps_from_a_to_z(directions, nodes):
    position = "AAA"
    pointer = 0
    while position != "ZZZ":
        position = nodes[position][int(directions[pointer % len(directions)])]
        pointer += 1
    return pointer


def get_starting_positions(nodes):
    """Return list of starting positions"""
    return [node for node in nodes if node[-1] == "A"]


def steps_from_a_to_z_modulo(directions, nodes):
    positions = get_starting_positions(nodes)
    end_points = []
    for position in positions:
        pointer = 0
        while position[-1] != "Z":
            position = nodes[position][int(directions[pointer % len(directions)])]
            pointer += 1
        print(position, pointer)
        end_points.append(pointer)
    return math.lcm(*end_points)


def steps_from_a_to_z_modulo2(directions, nodes):
    positions = get_starting_positions(nodes)
    for position in positions:
        pointer = 0
        outcomes = []
        while len(outcomes) < 10:
            position = nodes[position][int(directions[pointer % len(directions)])]
            pointer += 1
            if position[-1] == "Z":
                outcomes.append((pointer, position))
        print(outcomes)
    return pointer


def all_at_z(positions):
    for position in positions:
        if position[-1] != "Z":
            return False
    return True


def steps_from_a_to_z_2(directions, nodes):
    positions = get_starting_positions(nodes)
    pointer = 0
    while not all_at_z(positions):
        new_positions = []
        for position in positions:
            new_position = nodes[position][int(directions[pointer % len(directions)])]
            new_positions.append(new_position)
        pointer += 1
        if pointer % 10_000_000 == 0:
            print(pointer)
    return pointer


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
