class Hashmap:
    def _init_(self):
        self._hashmap = {i: [] for i in range(256)}

    def add(self, value, location):
        self._hashmap[hash(location)].append((location, value))

    def remove(self, value, location):
        self._hashmap[hash(location)].remove((location, value))

    @classmethod
    def hasher(cls, value) -> int:
        """Compute Hash of given value"""
        current_value = 0
        for character in value:
            current_value += ord(character)
            current_value *= 17
            current_value %= 256
        return current_value
