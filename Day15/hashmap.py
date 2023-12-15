class Hashmap:
    """Represents Hashmap"""

    def __init__(self):
        self._hashmap = [[] for _ in range(256)]

    def set(self, label, value):
        """Add value at location"""
        location = self.hasher(label)
        for slot, stored in enumerate(self._hashmap[location]):
            stored_label = stored[0]
            if label == stored_label:
                self._hashmap[location][slot] = (label, value)
                return
        self._hashmap[location].append((label, value))

    def remove(self, label):
        """remove value from location"""
        location = self.hasher(label)
        for stored_label, value in self._hashmap[location]:
            if label == stored_label:
                self._hashmap[location].remove((label, value))

    @property
    def score(self):
        """Compute score"""
        total = 0
        for number, contents in enumerate(self._hashmap):
            for slot, stored in enumerate(contents):
                focal_length = stored[1]
                total += (number + 1) * (slot + 1) * focal_length
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
