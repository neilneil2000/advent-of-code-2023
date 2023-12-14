from day14_input import day14_input


def main():
    platform = [list(row) for row in day14_input.splitlines()]
    display_platform(platform)
    platform = slider(platform)
    display_platform(platform)
    print(score(platform))


def slider(platform):
    new_platform = []
    for row in transpose(platform):
        data = "".join(row).split("#")
        new_row = []
        for chunk in data:
            # print(sorted(chunk, reverse=True))
            new_row.extend(sorted(chunk, reverse=True))
            new_row.append("#")
        new_row.pop()
        new_platform.append(new_row)
    return transpose(new_platform)


def score(platform):
    total = 0
    for index, row in enumerate(platform[::-1]):
        total += (index + 1) * row.count("O")
    return total


def display_platform(platform):
    for row in platform:
        print("".join(row))
    print()


def transpose(matrix):
    return list(zip(*matrix))


if __name__ == "__main__":
    main()
