from day8_input import day8_input

# day8_input = day8_input2


def main():
    directions, nodes = parse_input()
    steps = steps_from_a_to_z(directions, nodes)
    print(steps)


def steps_from_a_to_z(directions, nodes):
    position = "AAA"
    pointer = 0
    while position != "ZZZ":
        position = nodes[position][int(directions[pointer % len(directions)])]
        pointer += 1
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
