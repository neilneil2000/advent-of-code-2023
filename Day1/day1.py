"""Day 1 Advent of Code 2023"""

from day1_input import input_text

numbers = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def main():
    answer_part1 = 0
    answer_part2 = 0
    for line in input_text.splitlines():
        answer_part1 += get_calibration_value_part1(line)
        answer_part2 += get_calibration_value_part2(line)
    print(answer_part1)
    print(answer_part2)


def get_calibration_value_part1(line: str) -> int:
    """Compute calibration value from text line"""
    calibration_text = ""
    calibration_text = get_first_digit(line)
    calibration_text += get_first_digit(line[::-1])
    return int(calibration_text)


def get_calibration_value_part2(line: str) -> int:
    """Compute calibration value from text line"""
    calibration_text = ""
    calibration_text = get_first_number(line)
    calibration_text += get_last_number(line)
    return int(calibration_text)


def get_first_digit(line: str) -> str:
    """Return first numeric digit in line"""
    for letter in line:
        if letter.isnumeric():
            return letter


def get_first_number(line: str) -> int:
    """Return first numeric or written number in line"""
    cache = ""
    for letter in line:
        if letter.isnumeric():
            return letter
        cache += letter
        while cache not in [key[: len(cache)] for key in numbers]:
            if len(cache) == 1:
                cache = ""
                break
            cache = cache[1:]
        if cache in numbers:
            return str(numbers[cache])


def get_last_number(line: str) -> int:
    """Return last numeric or written number in line"""
    cache = ""
    for letter in line[::-1]:
        if letter.isnumeric():
            return letter
        cache = letter + cache
        while cache not in [key[-len(cache) :] for key in numbers]:
            if len(cache) == 1:
                cache = ""
                break
            cache = cache[:-1]
        if cache in numbers:
            return str(numbers[cache])


if __name__ == "__main__":
    main()
