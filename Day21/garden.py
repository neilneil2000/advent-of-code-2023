from functools import cache
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

    def locations_after_steps(self, number_of_steps, wrap=False):
        """Returns the number of locations possible to be in after number_of_steps"""
        locations = {self.get_start()}
        for step in range(number_of_steps):
            locations = self.locations_after_one_step(locations, wrap)
            print(f"Step {step+1}: {len(locations)}")
        return len(locations)

    def locations_after_one_step(self, locations, wrap=False):
        """Returns new set of locations after one step"""
        new_locations = set()
        for location in locations:
            new_locations.update(self.adjacent_squares(location))
        if wrap:
            return {
                location for location in new_locations if not self.is_rock(location)
            }
        return {location for location in new_locations if self.is_valid(location)}

    @cache
    def adjacent_squares(self, location) -> Set:
        """Return set of"""
        x, y = location
        return {(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)}

    @cache
    def wrap_to_bounds(self, location):
        """Returns location when forced to be within bounds"""
        x, y = location
        return (x % self.width, y % self.length)

    def is_valid(self, location):
        """Returns true if location is valid"""
        return self.is_within_bounds(location) and not self.is_rock(location)

    def is_rock(self, location):
        """Return True if location contains a rock"""
        x, y = self.wrap_to_bounds(location)
        return self.layout[y][x] == "#"

    def is_within_bounds(self, location):
        """Return True isf location is within bounds of garden"""
        x, y = location
        return 0 <= x < self.width and 0 <= y < self.length
