from day15_input import day15_input


def main():
    instructions = [s for s in day15_input.split(",")]
    part1_result = part1(instructions)
    print(part1_result)


def part1(instructions):
    return sum(hash(c) for c in instructions)


def hash(instruction: str) -> int:
    current_value = 0
    for character in instruction:
        current_value += ord(character)
        current_value *= 17
        current_value %= 256
    return current_value


if __name__ == "__main__":
    main()
