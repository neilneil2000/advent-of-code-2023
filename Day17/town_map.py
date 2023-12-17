class TownMap:
    """Representation of Town Layout"""

    directions = ["<", "^", ">", "V"]

    def __init__(self, layout):
        self.layout = layout
        self.start = None
        self.start_direction = None
        self.target = None

    @property
    def length(self):
        return len(self.layout)

    @property
    def width(self):
        return len(self.layout[0])

    def set_start(self, location):
        self.start = location

    def set_target(self, location):
        self.target = location

    def set_start_direction(self, direction):
        self.start_direction = direction

    def get_best_route(self):
        """Return numerical value of best route"""
        result = self.move_and_update(999999999999, 0, [(self.start, ">", 0)])
        result = self.move_and_update(result, 0, [(self.start, "V", 0)])
        return result

    def move_and_update(self, best, total, path):
        location, direction, steps = path[-1]
        pass
        if total >= best:
            return 99999999999999
        if location == self.target:
            print(total)
            return total
        if steps < 3:
            new_location = self.move_in_direction(location, direction)
            if (
                self.is_within_bounds(new_location)
                and (new_location, direction, steps + 1) not in path
            ):
                x, y = new_location
                value = self.layout[y][x]
                result = self.move_and_update(
                    best,
                    total + value,
                    path + [(new_location, direction, steps + 1)],
                )
                best = min(best, result)

        new_direction = self.turn_left(direction)
        new_location = self.move_in_direction(location, new_direction)
        if (
            self.is_within_bounds(new_location)
            and (new_location, new_direction, 1) not in path
        ):
            x, y = new_location
            value = self.layout[y][x]
            result = self.move_and_update(
                best,
                total + value,
                path + [(new_location, new_direction, 1)],
            )
            best = min(best, result)
        new_direction = self.turn_right(direction)
        new_location = self.move_in_direction(location, self.turn_right(direction))
        if (
            self.is_within_bounds(new_location)
            and (new_location, new_direction, 1) not in path
        ):
            x, y = new_location
            value = self.layout[y][x]
            result = self.move_and_update(
                best,
                total + value,
                path + [(new_location, new_direction, 1)],
            )
            best = min(best, result)
        return best

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

    def is_within_bounds(self, location):
        x, y = location
        return 0 <= x < self.width and 0 <= y < self.length
