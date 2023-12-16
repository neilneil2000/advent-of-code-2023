"""Cavern Floor class for Advent of Code 2023 Day 16"""

from functools import cache
from typing import Set, Tuple


class CavernFloor:
    """Representation of Cavern Floor"""

    def __init__(self, layout):
        self.layout = layout

    @property
    def _width(self):
        """Width of cavern floor"""
        return len(self.layout[0])

    @property
    def _length(self):
        """Length of cavern floor"""
        return len(self.layout)

    def display(self, energised=None):
        """Display energised locations"""
        locations = {entry[0] for entry in energised}
        for y in range(self._length):
            print("".join(self.layout[y]), end="\t")
            if energised is not None:
                for x in range(self._width):
                    if (x, y) in locations:
                        print("#", end="")
                    else:
                        print(".", end="")
            print("\n", end="")
        print()

    def energised_squares(self, location: Tuple[int] = None, direction=None) -> int:
        """Return all energised squares in layout"""
        if location is None:
            location = (0, 0)
        if direction is None:
            direction = ">"
        light_path = self._execute({(location, direction)})
        return len({entry[0] for entry in light_path})

    def most_energised_squares(self) -> int:
        """Return highest number of energised squares possible for layout"""
        best = 0

        for x in range(self._width):
            best = max(best, self.energised_squares((x, 0), "V"))
            best = max(best, self.energised_squares((x, self._length - 1), "^"))

        for y in range(self._length):
            best = max(best, self.energised_squares((0, y), ">"))
            best = max(best, self.energised_squares((self._width - 1, 0), "<"))

        return best

    def _execute(self, starting_beams: Set) -> Set:
        all_beams = starting_beams.copy()
        new_beams = self._move_beams(starting_beams)
        while new_beams:
            all_beams.update(new_beams)
            # self.display(all_beams)
            new_beams = self._move_beams(new_beams)
            new_beams = new_beams.difference(all_beams)
        return all_beams

    def _move_beams(self, beams) -> Set:
        """Return set of all locations and directions of light beam after moving them one square on"""
        new_beams = set()
        for location, direction in beams:
            new_beams.update(self._move_beam(location, direction))

        return {
            (location, direction)
            for location, direction in new_beams
            if self.in_range(location)
        }

    def in_range(self, location: Tuple[int, int]) -> bool:
        """Returns True if location is within layout"""
        x, y = location
        if 0 <= x < self._width and 0 <= y < self._length:
            return True
        return False

    def _light_beam(self, beams, all_beams=None) -> Set:
        """Return set of all locations and directions of light beam"""
        if not beams:
            return all_beams
        new_beams = set()
        for location, direction in beams:
            new_beams.update(self._move_beam(location, direction))

        for location, direction in new_beams.copy():
            x, y = location
            if 0 <= x < self._width and 0 <= y < self._length:
                continue
            new_beams.remove((location, direction))
        if all_beams is None:
            all_beams = beams.copy()
        all_beams.update(beams)

        return self._light_beam(new_beams, all_beams)

    @staticmethod
    def _reflect_beam(mirror: str, direction: str):
        resulting_beams = {
            ">": {".": {">"}, "/": {"^"}, "\\": {"V"}, "|": {"^", "V"}, "-": {">"}},
            "<": {".": {"<"}, "/": {"V"}, "\\": {"^"}, "|": {"^", "V"}, "-": {"<"}},
            "^": {".": {"^"}, "/": {">"}, "\\": {"<"}, "|": {"^"}, "-": {"<", ">"}},
            "V": {
                ".": {"V"},
                "/": {"<"},
                "\\": {">"},
                "|": {"V"},
                "-": {"<", ">"},
            },
        }
        return resulting_beams[direction][mirror]

    @staticmethod
    def _compute_beam(location, direction):
        """Move beam one step in diretion"""
        x, y = location
        new_location = (x, y + 1)
        if direction == ">":
            new_location = (x + 1, y)
        elif direction == "<":
            new_location = (x - 1, y)
        elif direction == "^":
            new_location = (x, y - 1)
        return new_location, direction

    @staticmethod
    def __move_beam(location, direction, mirror, reflect, compute):
        new_beams = set()
        for new_direction in reflect(mirror, direction):
            new_beams.add(compute(location, new_direction))

        return new_beams

    def _move_beam(self, location: Tuple[int], direction: str) -> Set:
        """Returns set of locations that a given beam moves to"""
        x, y = location
        mirror = self.layout[y][x]

        return self.__move_beam(
            location, direction, mirror, self._reflect_beam, self._compute_beam
        )
