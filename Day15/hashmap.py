"""Hashmap Class for AoC2023 Day 15"""
from collections import OrderedDict


class Hashmap:
    """Represents Hashmap"""

    def __init__(self):
        self._hashmap = [OrderedDict() for _ in range(256)]

    def set(self, label, value):
        """Add value at location"""
        location = self.hasher(label)
        self._hashmap[location][label] = value

    def remove(self, label):
        """remove value from location"""
        location = self.hasher(label)
        self._hashmap[location] = OrderedDict(
            (k, v) for k, v in self._hashmap[location].items() if k != label
        )

    @property
    def score(self):
        """Compute score"""
        total = 0
        for number, contents in enumerate(self._hashmap):
            for slot, stored in enumerate(contents.items()):
                total += (number + 1) * (slot + 1) * stored[1]
        return total

    @classmethod
    def hasher(cls, value) -> int:
        """Compute Hash of given value"""
        current_value = 0
        for character in value:
            current_value += ord(character)
            current_value *= 17
            current_value %= 256
        return current_value
