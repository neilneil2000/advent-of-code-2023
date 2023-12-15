"""Advent of Code 2023 Day 6"""


def main():
    part1_data = [(60, 475), (94, 2138), (78, 1015), (82, 1650)]
    part2_data = [(60947882, 475213810151650)]
    # print(ways_to_win(part1_data))
    print(f"Part 1: {ways_to_win_fast(part1_data)}")
    # print(ways_to_win(part2_data))
    print(f"Part 2: {ways_to_win_fast(part2_data)}")


def ways_to_win(input_data) -> int:
    """Return number of ways to win with given input data O(n)"""
    total = 1
    for max_time, target_distance in input_data:
        ways = 0
        for time in range(max_time):
            distance = time * (max_time - time)
            if distance > target_distance:
                ways += 1
        total *= ways
    return total


def ways_to_win_fast(input_data) -> int:
    """Return number of ways to win with given input data O(1)"""
    total = 1
    for max_time, target_distance in input_data:
        a = -1
        b = max_time
        c = -target_distance

        d = (b**2) - (4 * a * c)

        sol1 = (-b + (d**0.5)) / (2 * a)
        sol2 = (-b - (d**0.5)) / (2 * a)

        total *= int(sol2) - int(sol1)

    return total


if __name__ == "__main__":
    main()
