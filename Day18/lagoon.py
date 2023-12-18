class Lagoon:
    """Representation of a Lagoon"""

    def __init__(self, instructions):
        self.instructions = instructions
        self.path = [(0, 0)]
        self.lagoon = None

    @property
    def digger(self):
        return self.path[-1]

    def dig_perimeter(self):
        """Dig Perimeter"""
        for direction, count, _ in self.instructions:
            digger_x, digger_y = self.digger
            if direction == "R":
                self.path.append((digger_x + count, digger_y))
            if direction == "L":
                self.path.append((digger_x - count, digger_y))
            if direction == "U":
                self.path.append((digger_x, digger_y - count))
            if direction == "D":
                self.path.append((digger_x, digger_y + count))

    def dig_internal(self):
        x_min = sorted(self.path)[0][0]
        x_max = sorted(self.path)[-1][0]
        y_min = sorted(list(zip(*self.path))[1])[0]
        y_max = sorted(list(zip(*self.path))[1])[-1]
        width = x_max - x_min + 3
        length = y_max - y_min + 3

        self.lagoon = [["." for _ in range(width)] for length in range(length)]

        last_x = None
        last_y = None
        for x, y in self.path:
            if last_x is not None and last_y is not None:
                if x == last_x:
                    low_y, high_y = sorted([y, last_y])
                    for intermediate in range(low_y, high_y):
                        self.lagoon[intermediate - y_min + 1][x - x_min + 1] = "#"
                else:
                    low_x, high_x = sorted([x, last_x])
                    for intermediate in range(low_x, high_x):
                        self.lagoon[y - y_min + 1][intermediate - x_min + 1] = "#"
            self.lagoon[y - y_min + 1][x - x_min + 1] = "#"
            last_x, last_y = x, y

    def display(self):
        for row in self.lagoon:
            print("".join(row))

    def flood_fill_outside(self):
        to_check = [(0, 0)]
        self.flood(to_check)

    def flood(self, to_check):
        next_check = []
        for x, y in to_check:
            if not self.is_within_bounds((x, y)) or self.lagoon[y][x] != ".":
                continue
            self.lagoon[y][x] = "O"
            next_check.extend([(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)])
        if next_check:
            self.flood(next_check)

    def is_within_bounds(self, location):
        x, y = location
        return 0 <= x < self.width and 0 <= y < self.length

    @property
    def volume(self):
        total = 0
        for row in self.lagoon:
            total += "".join(row).count(".")
            total += "".join(row).count("#")
        return total

    @property
    def length(self):
        return len(self.lagoon)

    @property
    def width(self):
        return len(self.lagoon[0])
