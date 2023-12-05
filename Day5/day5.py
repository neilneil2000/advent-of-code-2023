"""Advent of Code 2023 Day 5"""

from day5_input import day5_input

def main():
    seeds, maps = parse_input()
    locations = execute_part1(seeds, maps)
    print(locations)
    print(min(locations))

def parse_input():
    chunks = day5_input.split("\n\n")
    seeds = chunks[0].split(":")[1].split()
    seeds = [int(seed) for seed in seeds]
    maps= []
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
        output_data=[]
        for datum in input_data:
            output_data.append(mapper(datum, map))
        input_data = output_data.copy()
    return output_data

def mapper(datum, map):
    for dest, source, number in map:
        if datum not in range(source, source+number):
            continue
        step=dest-source
        return datum+step
    return datum



if __name__ == "__main__":
    main()