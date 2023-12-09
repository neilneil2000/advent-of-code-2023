from typing import List

from day9_input import day9_input

def main():
    processed=parse_input()
    part1_answer=get_total(processed)
    print(f"Part 1 Answer: {part1_answer}")
    part2_answer=get_total(processed,True)
    print(f"Part 2 Answer: {part2_answer}")

def parse_input():
    rows = day9_input.splitlines()
    processed=[]
    for row in rows:
        processed.append(list(map(int,row.split())))
    return processed

def next_value(working_data:List)-> int:
    """Get next_value in sequence"""
    for row in working_data[::-1]:
        if len(set(row))==1:
            value=row[0]
            continue
        value = row[-1]+value
    return value

def previous_value(working_data:List)-> int:
    """Get next_value in sequence"""
    for row in working_data[::-1]:
        if len(set(row))==1:
            value=row[0]
            continue
        value = row[0]-value
    return value

def build_all_rows(sequence:List)->List:
    """Return list of all rows until differences is all zeroes"""
    current_row = sequence.copy()
    
    working_data=[current_row]
    while set(current_row)!={0}:
        current_row=get_differences(current_row)
        working_data.append(current_row)
    return working_data



def get_differences(sequence:List)->List:
    """Returns a list of differences between entries in input list"""
    return [sequence[i+1]-sequence[i] for i in range(len(sequence)-1)]

def get_total(input_data:List, backwards:bool=False)->int:
    """Compute Total for each part. Set backwards=True for part 2"""
    process=previous_value if backwards else next_value
    return sum(process(build_all_rows(sequence)) for sequence in input_data)

    



if __name__=="__main__":
    main()