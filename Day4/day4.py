"""Advent of Code 2023 Day 4"""
from typing import List, Set
from day4_input import input_scratchcards


def main():
    """Main Program"""
    scratchcards = parse_input(input_scratchcards)

    part1_result = part_one(scratchcards)
    print(f"Answer to Part1 : {part1_result}")

    part2_result = part_two(scratchcards)
    print(f"Answer to Part2 : {part2_result}")


def part_one(scratchcards: List[Set]) -> int:
    """Calculate Result for Part 1"""
    return sum(calculate_score(scratchcard) for scratchcard in scratchcards)


def part_two(scratchcards: List[Set]) -> int:
    """Calculate Result for Part 2"""
    totals = [1 for _ in scratchcards]
    score = 0
    game_number = 0
    for card in scratchcards:
        score = count_matches(card)
        if score:
            for _ in range(totals[game_number]):
                for number in range(game_number + 1, game_number + score + 1):
                    totals[number] += 1
        game_number += 1
    return sum(totals)


def parse_input(input_cards: List[str]) -> List[Set]:
    """Parse input file into structured output"""
    scratchcards = []
    for card in input_cards.splitlines():
        _, numbers = card.split(":")
        winners, yours = numbers.split("|")
        scratchcards.append((set(winners.split()), set(yours.split())))
    return scratchcards


def count_matches(scratchcard: List[Set]) -> int:
    """Return number of entries in common between two number sets"""
    return len(scratchcard[0].intersection(scratchcard[1]))


def calculate_score(card):
    """
    Return Score of a scratchcard according to pattern:

    MATCHES | 0  1  2  3  4  ...
    SCORE   | 0  2  4  8  16 ...

    """
    if matches := count_matches(card):
        return 2 ** (matches - 1)
    return 0


if __name__ == "__main__":
    main()
