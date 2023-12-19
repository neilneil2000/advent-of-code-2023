class Lagoon:
    """Representation of a Lagoon"""

    def __init__(self, instructions):
        self.instructions = instructions
        self.path = [(0, 0)]
        self.lagoon = None
        self.vertices = None

    @property
    def digger(self):
        return self.path[-1]

    def dig_perimeter(self):
        """Dig Perimeter"""
        self.path = [(0, 0)]
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

    def convert_hex_instructions(self):
        new_instructions = []
        directions = {"0": "R", "1": "D", "2": "L", "3": "U"}
        for _, _, hex_code in self.instructions:
            distance = int(hex_code[:5], 16)
            direction = directions[hex_code[-1]]
            new_instructions.append((direction, distance, ""))
        self.instructions = new_instructions

    def build_vertices(self):
        self.vertices = {}
        for x, y in self.path:
            if y not in self.vertices:
                self.vertices[y] = set()
            self.vertices[y].add(x)

    def compute_volume(self):
        total = 0
        calc_rows = []
        for row, vertices in sorted(self.vertices.items()):
            collapsed = []
            for calc_row, start, end in calc_rows.copy():
                if start not in vertices and end not in vertices:
                    continue
                collapsed.append([start, end])
                calc_rows.remove((calc_row, start, end))
                row_length = end - start + 1
                row_depth = row - calc_row
                total += row_length * row_depth
            for index, vertex in enumerate(sorted(vertices)):
                if collapsed:
                    start, end = collapsed.pop(0)
                    if vertex < start < end:
                        # add e to current row and remove s from row
                        vertices.add(end)
                        vertices.remove(start)
                    elif start < vertex < end:
                        # add s to row and remove e from row
                        vertices.add(start)
                        vertices.remove(end)
                        # increase total by e-vertex
                        total += end - vertex
                    elif start == vertex:
                        total += sorted(vertices)[index + 1] - vertex
                        # remove vertex and add e
                        vertices.add(end)
                        vertices.remove(vertex)
                    else:
                        # add s to row and remove vertex from row
                        vertices.add(start)
                        vertices.remove(vertex)
            vertex_pairs = [
                sorted(vertices)[i : i + 2] for i in range(0, len(vertices), 2)
            ]
            for a, b in vertex_pairs:
                calc_rows.append((row, a, b))
            pass

        return total

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

    def volume_of_next_chunk(self):
        b, c = self.get_start_line()
        if c == len(self.path) - 1:
            c = 0
        a = self.path[b - 1]
        d = self.path[(c + 1)]

        total = 0
        if a[0] > d[0]:
            total += (abs(self.path[c][1] - d[1]) + 1) * (abs(a[0] - self.path[b][0]))
            self.path[b] = (d[0], self.path[b][1])
            if c == 0:
                self.path[len(self.path) - 1] = (d[0], self.path[c][1])
            self.path.pop(c)
            self.path.pop(c)
        else:
            total += (abs(a[1] - self.path[b][1]) + 1) * (abs(a[0] - self.path[b][0]))
            self.path[c] = (a[0], self.path[c][1])
            if c == 0:
                self.path[len(self.path) - 1] = (a[0], self.path[c][1])
            self.path.pop(b)
            self.path.pop(b - 1)
        self.dig_internal()
        return total

    def get_start_line(self):
        x_min = sorted(self.path)[0][0]
        # find something that touches x_min
        anchor = None
        end_point = None
        for index, location in enumerate(self.path):
            x, _ = location
            if x != x_min:
                anchor = None
                continue
            if anchor is None:
                anchor = index
                continue
            if x != self.path[anchor][0]:  # movement in x
                anchor = None
                continue
            end_point = index
            break
        return anchor, end_point

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
