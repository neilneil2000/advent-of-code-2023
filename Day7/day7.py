from typing import List, Tuple

from day7_input import day7_input


def main():
    rounds = input_processor()

    part_1 = get_total(rounds)
    print(f"Part1: {part_1}")
    part_2 = get_total(rounds, True)
    print(f"Part2: {part_2}")


def get_total(rounds, consider_jokers=False) -> int:
    """Return total value for all poker hands"""
    categories = [[] for _ in range(7)]  # 7 categories
    for hand, bid in rounds:
        if consider_jokers:
            hand = hand.replace("D", "P")
        categories[sorting_hat_with_jokers(hand, consider_jokers)].append((hand, bid))
    all_hands = []
    for category in categories:
        all_hands.extend(sorted(category))
    total = 0
    for index, hand in enumerate(all_hands[::-1]):
        total += hand[1] * (index + 1)
    return total


def sorting_hat_with_jokers(hand: str, consider_jokers=False) -> int:
    """Returns best hand rank and can considering jokers"""
    best_result = sorting_hat(hand)
    if not consider_jokers:
        return best_result

    joker = "P"
    if joker not in hand:
        return best_result

    for card in ["A", "B", "C", "E", "F", "G", "H", "I", "L", "M", "N", "O"]:
        best_result = min(best_result, sorting_hat(hand.replace(joker, card)))
    return best_result


def sorting_hat(hand: str) -> int:
    """Returns value from 0 to 6 determining primary strength of hand"""
    counts = {}
    for character in set(hand):
        counts[character] = hand.count(character)
    maximum = max(counts.values())
    if maximum == 5:
        return 0  # Five of a Kind
    if maximum == 4:
        return 1  # Four of a Kind
    if maximum == 3 and len(counts) == 2:
        return 2  # Full House
    if maximum == 3:
        return 3  # Three of a kind
    if maximum == 2 and len(counts) == 3:
        return 4  # Two Pair
    if maximum == 2:
        return 5  # One Pair
    return 6  # High Card


def input_processor() -> List[Tuple[str, int]]:
    """Convert Cards to Coded Version to exploit built in sort functions and provide structured output"""
    cards = ["K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    coded_cards = ["B", "C", "D", "E", "F", "G", "H", "I", "L", "M", "N", "O"]
    card_map = list(zip(cards, coded_cards))

    processed_hands = []
    for row in day7_input.splitlines():
        hand, bid = row.split()
        for old, new in card_map:
            hand = hand.replace(old, new)
        processed_hands.append((hand, int(bid)))
    return processed_hands


if __name__ == "__main__":
    main()
