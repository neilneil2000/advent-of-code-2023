from typing import Tuple,List
from day10_input import day10_input

def main():
    metal_map=parse_input()
    print(metal_map)
    part1(metal_map)

def part1(m):
    steps={-1:set()}
    for y in range(len(m)):
        for x in range(len(m[0])):
            steps[-1].add((x,y))
    start=get_start_coordinate(m)
    steps[-1].remove(start)
    value=0
    in_play={start}
    steps[value]=in_play
    while in_play:
        value+=1
        steps[value]=set()
        in_play=update_steps(in_play, steps, m,value)
    if steps[value] ==set():
        del steps[value]
    print(max(steps.keys()))


    

def update_steps(starting_points, steps, m,value):
    next_spaces=set()
 # print(f"From: {starting_points}")
    for point in starting_points:
        next_spaces.update(update_neighbours(point, steps,m,value))
  #print(f"To: {next_spaces}\n")
    return next_spaces


def get_valid_neighbours(point:Tuple[int],metal_map:List[List[str]])-> Tuple:
    """Returns Valid Neighbours for point
    Where you can go from a given square depends on the content of that square
    """
    x,y=point
    up=(x,y-1)
    down=(x,y+1)
    left=(x-1,y)
    right=(x+1,y)
    symbol =metal_map[y][x]
    if symbol =="S":
        return up,down,left,right
    if symbol == "|":
        return up,down,None, None
    if symbol == "-":
        return None, None,left,right
    if symbol == "L":
        return up,None,None, right
    if symbol == "J":
        return up,None,left, None
    if symbol == "7":
        return None,down,left, None
    if symbol == "F":
        return None,down,None, right
    return None, None, None, None
    
  



def update_neighbours(point, steps, m,value):
    up_valid=['|','7','F']
    down_valid=['|', 'L', 'J']
    left_valid=['-','L','F']
    right_valid=['-','J','7']
    up, down, left, right =get_valid_neighbours(point,m)
    next_spaces=set()
  #print(m[up[1]][up[0]])
    if up in steps[-1] and m[up[1]][up[0]] in up_valid:
        steps[value].add(up)
        steps[-1].remove(up)
        next_spaces.add(up)
    
    if down in steps[-1] and m[down[1]][down[0]] in down_valid:
        steps[value].add(down)
        steps[-1].remove(down)
        next_spaces.add(down)

    if left in steps[-1] and m[left[1]][left[0]] in left_valid:
        steps[value].add(left)
        steps[-1].remove(left)
        next_spaces.add(left)

    if right in steps[-1] and m[right[1]][right[0]] in right_valid:
        steps[value].add(right)
        steps[-1].remove(right)
        next_spaces.add(right)

    return next_spaces
  
    

def get_start_coordinate(m):
    for y in range(len(m)):
        for x in range(len(m[y])):
            if m[y][x] == 'S':
                return (x,y)

def parse_input():
    metal_map=[]
    for line in day10_input.splitlines():
        metal_map.append(list(line))
    return metal_map



if __name__ == '__main__':
    main()