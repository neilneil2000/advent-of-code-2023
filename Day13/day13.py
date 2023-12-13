from day13_input import day13_input


def get_row_reflection(landscape):
    """Return row of reflection"""
    for index, _ in enumerate(landscape):
        if index == 0:
            continue
        for top, bottom in zip(landscape[:index][::-1], landscape[index:]):
            flag = True
            print("".join(top))
            print("".join(bottom))
            if top is None:
                return index
            if bottom is None:
                return index
            if top != bottom:
                flag = False
                break
        if flag:
            return index

    return 0


def display_landscape(landscape):
    for row in landscape:
        print("".join(row))


def transpose(landscape):
    return list(zip(*landscape))


def parse_input():
    chunks = day13_input.split("\n\n")
    landscapes = []
    for chunk in chunks:
        landscape = chunk.splitlines()
        landscapes.append([list(row) for row in landscape])
    return landscapes


def part1(landscapes):
    row_total = 0
    column_total = 0
    for landscape in landscapes:
        row = get_row_reflection(landscape)
        row_total += row
        if not row:
            column_total += get_row_reflection(transpose(landscape))
    return row_total * 100 + column_total


def main():
    parsed = parse_input()
    result = part1(parsed)
    print(result)


if __name__ == "__main__":
    main()
