from day25_test_input import day25_input
from snow_machine import SnowMachine


def main():
    data = parse_input()
    bertha = SnowMachine(data)
    chunks = bertha.count_chunks()
    print(chunks)


def parse_input():
    """Return structured representation of input"""
    parsed = {}
    for line in day25_input.splitlines():
        a, b = line.split(":")
        b = b.split()
        parsed[a] = b
    return parsed


if __name__ == "__main__":
    main()
