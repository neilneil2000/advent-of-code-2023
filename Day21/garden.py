from typing import Set


class Garden:
    """Representation of garden"""

    def __init__(self, layout):
        self.layout = layout

    def get_start(self):
        """Return start location"""
        for y, row in enumerate(self.layout):
            for x, character in enumerate(row):
                if character == "S":
                    return (x, y)
        return (-1, -1)

    @property
    def width(self):
        return len(self.layout[0])

    @property
    def length(self):
        return len(self.layout)

    def locations_after_steps(self, number_of_steps):
        """Returns the number of locations possible to be in after number_of_steps"""
        locations = {self.get_start()}
        for _ in range(number_of_steps):
            locations = self.locations_after_one_step(locations)
        return len(locations)

    def locations_after_one_step(self, locations):
        """Returns new set of locations after one step"""
        new_locations = set()
        for location in locations:
            new_locations.update(self.adjacent_squares(location))
        return {location for location in new_locations if self.is_valid(location)}

    def adjacent_squares(self, location) -> Set:
        """Return set of"""
        x, y = location
        return {(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)}

    def is_valid(self, location):
        """Returns true if location is valid"""
        return self.is_within_bounds(location) and not self.is_rock(location)

    def is_rock(self, location):
        """Return True if location contains a rock"""
        x, y = location
        return self.layout[y][x] == "#"

    def is_within_bounds(self, location):
        """Return True isf location is within bounds of garden"""
        x, y = location
        return 0 <= x < self.width and 0 <= y < self.length
