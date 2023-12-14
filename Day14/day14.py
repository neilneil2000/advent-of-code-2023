"""Advent of Code 2023 Day 14"""
from typing import List
from functools import cache
from day14_input import day14_input


def main():
    """Main Solution Loop"""
    starting_position = parse_input()
    part1_result = part1(starting_position)
    print(f"Part 1: {part1_result}")

    part2_result = part2(starting_position)
    print(f"Part 2: {part2_result}")


def part1(starting_position):
    """Compute Part 1"""
    current_position = slide(starting_position, "North")
    return score(current_position)


def part2(starting_position):
    """Compute Part 2"""
    current_position = spin(starting_position)
    results = [score(current_position)]
    while not (period := repeat_period(results)):
        current_position = spin(current_position)
        results.append(score(current_position))
    return get_score_at(results, period, 1_000_000_000)


def parse_input():
    """Return structured representation of input data"""
    return [list(row) for row in day14_input.splitlines()]


def get_score_at(results: List[int], period: int, target_entry: int) -> int:
    """Return extrapolated score at target_entry"""
    return results[-(period - ((target_entry - len(results)) % period)) - 1]


def repeat_period(results: List[int]) -> int:
    """
    Returns period of repeat if there is a repeating pattern of results
    Note: returns 0 if no repeat period found
    """
    min_matches = 5
    max_chunk_size = len(results) // min_matches
    if max_chunk_size < 1:
        return 0
    for chunk_size in range(1, max_chunk_size + 1):
        chunks = [
            results[i : i + chunk_size] for i in range(0, len(results), chunk_size)
        ]
        if chunks[-1] == chunks[-2] == chunks[-3] == chunks[-4] == chunks[-5]:
            return chunk_size

    return 0


def spin(platform: List[List[str]]):
    """Emulate a spin of the platform, tilting once in each direction"""
    platform = slide(platform, "North")
    platform = slide(platform, "West")
    platform = slide(platform, "South")
    platform = slide(platform, "East")
    return platform


def slide(platform: List[List[str]], direction: str) -> List[List[str]]:
    """Tilt platform in a direction and calculate new positions of boulders"""
    if direction == "North":
        return transpose(slider(transpose(platform)))
    if direction == "West":
        return slider(platform)
    if direction == "South":
        return transpose(slider(transpose(platform), to_the_left=False))
    return slider(platform, to_the_left=False)


def slider(platform: List[List[str]], to_the_left: bool = True):
    """Slide boulders in one direction"""
    new_platform = []
    for row in platform:
        data = "".join(row).split("#")
        new_row = []
        for chunk in data:
            new_row.extend(sorted(chunk, reverse=to_the_left))
            new_row.append("#")
        new_platform.append(new_row[:-1])
    return new_platform


def score(platform: List[List[str]]):
    """Calculate Load on North Beam (aka score)"""
    total = 0
    for index, row in enumerate(platform[::-1]):
        total += (index + 1) * row.count("O")
    return total


def display_platform(platform: List[List[str]]):
    """Print Platform Layout to screen"""
    for row in platform:
        print("".join(row))
    print()


def transpose(matrix):
    """Transpose a 2D Array"""
    return list(zip(*matrix))


if __name__ == "__main__":
    main()
