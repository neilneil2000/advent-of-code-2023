"""Advent of Code 2023 Day 5"""

from typing import Tuple, List

from day5_input import day5_input


def main():
    seeds, maps = parse_input()
    locations = execute_part1(seeds, maps)
    print(f"Part 1 Lowest location is {min(locations)}")

    seeds = reprocess_seeds(seeds)
    smallest_location = execute_part2(seeds, maps)
    print(f"Part 2 Lowest location is {smallest_location}")


def reprocess_seeds(old_seeds):
    new_seeds = []
    cache = 0
    for index, entry in enumerate(old_seeds):
        if index % 2 == 0:
            cache = entry
        else:
            new_seeds.append((cache, entry + cache - 1))

    return new_seeds


def parse_input():
    chunks = day5_input.split("\n\n")
    seeds = chunks[0].split(":")[1].split()
    seeds = [int(seed) for seed in seeds]
    maps = []
    for chunk in chunks[1:]:
        map_entries = chunk.splitlines()
        p_map_entries = []
        for map_entry in map_entries[1:]:
            processed_entry = map_entry.split()
            p_map_entries.append([int(entry) for entry in processed_entry])
        maps.append(p_map_entries)
    return seeds, maps


def execute_part1(input_data, maps):
    for map in maps:
        output_data = []
        for datum in input_data:
            output_data.append(mapper(datum, map))
        input_data = output_data.copy()
    return output_data


def execute_map_row(data, data_map):
    """Execute a Mapping Row against full unprocessed data set"""
    mapped_data = set()
    unmatched = set()
    for data_range in data:
        processed, unprocessed = get_overlap(data_range, data_map)
        unmatched.update(unprocessed)
        if processed is not None:
            mapped_data.add(processed)
    return unmatched, mapped_data


def execute_part2(seeds, maps):
    unprocessed = set(seeds)

    for mapping_stage in maps:
        tracked_pro = set()
        for map_row in mapping_stage:
            unprocessed, processed = execute_map_row(unprocessed, map_row)
            tracked_pro.update(processed)
        unprocessed.update(tracked_pro)

    return get_lowest_location(unprocessed)


def get_lowest_location(locations):
    best = 999999999999
    for answer in locations:
        best = min(answer[0], best)
    return best


def get_overlap(data, data_map):
    # data/seeds = [79, 14]
    # data_map/seed_to_soil_map = [50, 98, 2]
    mapping_adder = data_map[0] - data_map[1]
    data_map_input_range = (
        data_map[1],
        data_map[1] + data_map[2] - 1,
    )
    overlap, unmatched = split_range_a_by_range_b(data, data_map_input_range)
    if not overlap:
        return None, set(unmatched)
    processed = (overlap[0] + mapping_adder, overlap[1] + mapping_adder)
    return processed, set(unmatched)


def test_function():
    seeds = [79, 14]
    seed_range = (seeds[0], sum(seeds) - 1)
    seed_to_soil_map = [50, 98, 2]
    mapping_adder = seed_to_soil_map[0] - seed_to_soil_map[1]
    seed_to_soil_input_range = (
        seed_to_soil_map[1],
        seed_to_soil_map[1] + seed_to_soil_map[2] - 1,
    )
    overlap, unmatched = split_range_a_by_range_b(seed_range, seed_to_soil_input_range)
    if not overlap:
        return unmatched
    overlap = (overlap[0] + mapping_adder, overlap[1] + mapping_adder)
    return unmatched.append(overlap)


def split_range_a_by_range_b(range_a: Tuple, range_b: Tuple) -> Tuple[Tuple]:
    """
    Split range_a into overlap and unmatched by range_b
    Returns Tuple of Overlap as a Tuple and List of Unmatched remainder of range_a
    """
    a_start, a_end = range_a
    b_start, b_end = range_b

    if a_end < b_start or a_start > b_end:  # no overlap
        return (), [range_a]

    if a_start >= b_start and a_end <= b_end:  # complete overlap
        return range_a, []

    unmatched = []
    if a_start < b_start:
        unmatched.append((a_start, b_start - 1))
    if a_end > b_end:
        unmatched.append((b_end + 1, a_end))

    return (max(a_start, b_start), min(a_end, b_end)), unmatched


def mapper(datum, map):
    for dest, source, number in map:
        if datum not in range(source, source + number):
            continue
        step = dest - source
        return datum + step
    return datum


if __name__ == "__main__":
    main()
