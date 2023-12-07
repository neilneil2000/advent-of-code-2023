from day7_input import day7_input


def main():
    rounds = input_processor()
    categories = [[] for _ in range(7)]  # 7 categories

    for hand, bid in rounds:
        categories[sorting_hat(hand)].append((hand, bid))
    all_hands = []
    for category in categories:
        all_hands.extend(sorted(category))
    print(all_hands)
    total = 0
    for index, hand in enumerate(all_hands[::-1]):
        total += hand[1] * (index + 1)
        print(hand[0], hand[1], index)
    print(total)

    categories = [[] for _ in range(7)]  # 7 categories
    for hand, bid in rounds:
        hand = hand.replace("D", "P")
        categories[sorting_hat_with_jokers(hand)].append((hand, bid))
    all_hands = []
    for category in categories:
        all_hands.extend(sorted(category))
    print(all_hands)
    total = 0
    for index, hand in enumerate(all_hands[::-1]):
        total += hand[1] * (index + 1)
        print(hand[0], hand[1], index)
    print(total)


def sorting_hat_with_jokers(hand: str) -> int:
    joker = "P"
    best_result = sorting_hat(hand)  # Ensure Joker is weakest
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


def input_processor():
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
