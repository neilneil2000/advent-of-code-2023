from typing import Dict, List
from day2_input import day2_input


def main():
    game_outcomes = parse_input()
    game_setup = {"red": 12, "green": 13, "blue": 14}
    possible_games = get_possible_games(game_outcomes, game_setup)
    # print(possible_games)
    print(f"Part 1: {sum(possible_games)}")

    powers = []
    for outcomes in game_outcomes.values():
        minimum_set = compute_minimum_set(outcomes)
        powers.append(compute_power(minimum_set))
    # print(powers)
    print(f"Part 2: {sum(powers)}")


def compute_minimum_set(outcomes: List):
    """Return minimum set of cubes required to play game"""
    minimum_set = {"red": 0, "green": 0, "blue": 0}
    for outcome in outcomes:
        for colour, number in outcome.items():
            minimum_set[colour] = max(minimum_set[colour], number)
    return minimum_set


def compute_power(cubes: Dict):
    "Return power of a given set of cubes, where power is the number of each cube multiplied together"
    power = 1
    for number in cubes.values():
        power *= number
    return power


def get_possible_games(outcomes: Dict, setup: Dict) -> List:
    """Return list of game outcomes that could have occured with the given setup"""
    possibles = []
    for current_game, outcome_set in outcomes.items():
        possible_flag = True
        for outcome in outcome_set:
            for colour, number in outcome.items():
                if setup[colour] < number:
                    possible_flag = False
                    break  # This outcome not valid
        if possible_flag:
            possibles.append(current_game)
    return possibles


def parse_input() -> Dict:
    """Parse input text and return structured objects"""
    games = {}
    for line in day2_input.splitlines():
        game_number, outcomes = parse_line(line)
        games[game_number] = outcomes
    return games


def parse_line(line: str):
    """Return Structured Object for one line in input
    Example => Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    """
    game_number, outcomes = line.split(":")
    _, game_number = game_number.split(" ")
    outcomes = outcomes.split(";")
    structured_outcomes = []
    for outcome in outcomes:
        colour_sets = outcome.split(",")
        structured_set = {}
        for colour_set in colour_sets:
            number, colour = colour_set.strip().split(" ")
            structured_set[colour] = int(number)
        structured_outcomes.append(structured_set)
    return int(game_number), structured_outcomes


if __name__ == "__main__":
    main()
