class TownMap:
    """Representation of Town Layout"""

    directions = ["<", "^", ">", "V"]

    def __init__(self, layout):
        self.layout = layout
        self.totals = {
            0: {
                "<": [[None for entries in row] for row in self.layout],
                "^": [[None for entries in row] for row in self.layout],
                ">": [[None for entries in row] for row in self.layout],
                "V": [[None for entries in row] for row in self.layout],
            },
            1: {
                "<": [[None for entries in row] for row in self.layout],
                "^": [[None for entries in row] for row in self.layout],
                ">": [[None for entries in row] for row in self.layout],
                "V": [[None for entries in row] for row in self.layout],
            },
            2: {
                "<": [[None for entries in row] for row in self.layout],
                "^": [[None for entries in row] for row in self.layout],
                ">": [[None for entries in row] for row in self.layout],
                "V": [[None for entries in row] for row in self.layout],
            },
            3: {
                "<": [[None for entries in row] for row in self.layout],
                "^": [[None for entries in row] for row in self.layout],
                ">": [[None for entries in row] for row in self.layout],
                "V": [[None for entries in row] for row in self.layout],
            },
        }
        self.start = None

    @property
    def length(self):
        return len(self.layout)

    @property
    def width(self):
        return len(self.layout[0])

    def set_start(self, location):
        self.start = location

    def get_best_at(self, location):
        """Return best value at location"""
        crucibles = [(self.start, ">", 0, 0), (self.start, "V", 0, 0)]
        while crucibles:
            crucibles = self.flood_fill(crucibles)

        x, y = location
        results = []
        for steps in [0, 1, 2, 3]:
            for direction in ["<", "V", ">", "^"]:
                if self.totals[steps][direction][y][x] is not None:
                    results.append(self.totals[steps][direction][y][x])
        return min(results)

    def flood_fill(self, crucibles):
        worthy_crucibles = set()
        for crucible in crucibles:
            if self._update_totals(crucible):
                worthy_crucibles.add(crucible)
        next_crucibles = set()
        for crucible in worthy_crucibles:
            next_crucibles.update(self.get_next_locations(crucible))

        return next_crucibles

    def get_next_locations(self, crucible):
        """Return next locations for input location"""
        location, direction, steps_forward, total = crucible
        next_crucibles = set()
        if steps_forward < 3:
            new_location = self.move_in_direction(location, direction)
            if self.is_within_bounds(new_location):
                x, y = new_location
                value = self.layout[y][x]
                new_crucible = (
                    new_location,
                    direction,
                    steps_forward + 1,
                    total + value,
                )
                next_crucibles.add(new_crucible)

        left = self.turn_left(direction)
        new_location = self.move_in_direction(location, left)
        if self.is_within_bounds(new_location):
            x, y = new_location
            value = self.layout[y][x]
            new_crucible = (new_location, left, 1, total + value)
            next_crucibles.add(new_crucible)

        right = self.turn_right(direction)
        new_location = self.move_in_direction(location, right)
        if self.is_within_bounds(new_location):
            x, y = new_location
            value = self.layout[y][x]
            new_crucible = (new_location, right, 1, total + value)
            next_crucibles.add(new_crucible)

        return {
            crucible
            for crucible in next_crucibles
            if self.is_within_bounds(crucible[0])
        }

    @classmethod
    def turn_left(cls, direction):
        return cls.directions[(cls.directions.index(direction) - 1) % 4]

    @classmethod
    def turn_right(cls, direction):
        return cls.directions[(cls.directions.index(direction) + 1) % 4]

    def move_in_direction(self, location, direction):
        x, y = location
        if direction == ">":
            return (x + 1, y)
        if direction == "<":
            return (x - 1, y)
        if direction == "^":
            return (x, y - 1)
        return (x, y + 1)

    def _update_totals(self, crucible):
        location, direction, steps, total = crucible
        x, y = location
        if (
            self.totals[steps][direction][y][x] is None
            or total < self.totals[steps][direction][y][x]
        ):
            self.totals[steps][direction][y][x] = total
            return True
        return False

    def is_within_bounds(self, location):
        x, y = location
        return 0 <= x < self.width and 0 <= y < self.length
