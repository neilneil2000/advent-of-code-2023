from typing import List

from day9_input import day9_input

def main():
    processed=parse_input()
    part1_answer=get_total(processed)
    print(f"Part 1 Answer: {part1_answer}")
    part2_answer=get_total(processed,True)
    print(f"Part 2 Answer: {part2_answer}")

def parse_input():
    return [list(map(int,row.split())) for row in day9_input.splitlines()]

def extrapolate(sequence, value,backwards:bool=False)->int:
    """Extrapolate sequence by value in direction indicated"""
    if backwards:
        return sequence[0]-value
    return sequence[-1]+value

def get_next_value(working_data:List, backwards=False)-> int:
    """Get next_value in sequence"""
    for row in working_data[::-1]:
        if len(set(row))==1:
            value=row[0]
            continue
        value = extrapolate(row,value, backwards)
    return value

def build_all_rows(sequence:List)->List:
    """Return list of all rows until differences is all zeroes"""
    working_data=[sequence]
    while set(working_data[-1])!={0}:
        working_data.append(get_differences(working_data[-1]))
    return working_data

def get_differences(sequence:List)->List:
    """Returns a list of differences between entries in input list"""
    return [sequence[i+1]-sequence[i] for i in range(len(sequence)-1)]

def get_total(input_data:List, backwards:bool=False)->int:
    """Compute Total for each part. Set backwards=True for part 2"""
    return sum(get_next_value(build_all_rows(sequence),backwards) for sequence in input_data)

    



if __name__=="__main__":
    main()