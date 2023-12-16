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

    def energised_squares(self, location: Tuple[int] = None, direction=None) -> Set:
        """Return all energised squares in layout"""
        if location is None:
            location = (0, 0)
        if direction is None:
            direction = ">"
        light_path = self._execute({(location, direction)})
        return len({entry[0] for entry in light_path})

    def most_energised_squares(self) -> int:
        """Return all energised squares in layout"""
        best = 0
        for x in range(self._width):
            light_path = self._execute({((x, 0), "V")})
            squares = {entry[0] for entry in light_path}
            best = max(best, len(squares))
            light_path = self._execute({((x, self._length - 1), "^")})
            squares = {entry[0] for entry in light_path}
            best = max(best, len(squares))

        for y in range(self._length):
            light_path = self._execute({((0, y), ">")})
            squares = {entry[0] for entry in light_path}
            best = max(best, len(squares))
            light_path = self._execute({((self._width - 1, y), "<")})
            squares = {entry[0] for entry in light_path}
            best = max(best, len(squares))

        return best

    def _execute(self, starting_beams: Set):
        all_beams = starting_beams.copy()
        new_beams = self._move_beams(starting_beams)
        while new_beams:
            all_beams.update(new_beams)
            # self.display(all_beams)
            new_beams = self._move_beams(new_beams)
            new_beams = new_beams.difference(all_beams)
        return all_beams

    def _move_beams(self, beams) -> Set:
        """Return set of all locations and directions of light beam"""
        new_beams = set()
        for location, direction in beams:
            new_beams.update(self._move_beam(location, direction))

        for location, direction in new_beams.copy():
            x, y = location
            if 0 <= x < self._width and 0 <= y < self._length:
                continue
            new_beams.remove((location, direction))

        return new_beams

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

    def _right(self, location) -> Tuple[Tuple[int], str]:
        """Moves beam towards right, returning location, direction Tuple"""
        x, y = location
        return (x + 1, y), ">"

    def _left(self, location) -> Tuple[Tuple[int], str]:
        """Moves beam towards right, returning location, direction Tuple"""
        x, y = location
        return (x - 1, y), "<"

    def _up(self, location) -> Tuple[Tuple[int], str]:
        """Moves beam towards right, returning location, direction Tuple"""
        x, y = location
        return (x, y - 1), "^"

    def _down(self, location) -> Tuple[Tuple[int], str]:
        """Moves beam towards right, returning location, direction Tuple"""
        x, y = location
        return (x, y + 1), "V"

    @cache
    def _move_beam(self, location: Tuple[int], direction: str) -> Set:
        """Returns set of locations that a given beam moves to"""
        x, y = location
        mirror = self.layout[y][x]
        left = self._left(location)
        right = self._right(location)
        up = self._up(location)
        down = self._down(location)
        resulting_beams = {
            ">": {".": {right}, "/": {up}, "\\": {down}, "|": {up, down}, "-": {right}},
            "<": {".": {left}, "/": {down}, "\\": {up}, "|": {up, down}, "-": {left}},
            "^": {".": {up}, "/": {right}, "\\": {left}, "|": {up}, "-": {left, right}},
            "V": {
                ".": {down},
                "/": {left},
                "\\": {right},
                "|": {down},
                "-": {left, right},
            },
        }

        return resulting_beams[direction][mirror]
