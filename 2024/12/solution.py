from datetime import datetime
from typing import Set, List, Tuple

def get_perimeter_of_cell(
        map: List[str], row: int, col: int, group_cells: List[Tuple[int, int]], visited: Set[Tuple[int,int]]) -> int:
    perimeter = 0
    visited.add((row, col))
    # print("Checking neighbors of {}, {}".format(row, col))
    # up
    if row == 0:
        perimeter += 1
    elif map[row-1][col] != map[row][col]:
        perimeter += 1
    elif (row-1, col) not in visited:
        group_cells.append((row-1, col))
    # down
    if row == len(map)-1:
        perimeter += 1
    elif map[row+1][col] != map[row][col]:
        perimeter += 1
    elif (row+1, col) not in visited:
        group_cells.append((row+1, col))
    # left
    if col == 0:
        perimeter += 1
    elif map[row][col-1] != map[row][col]:
        perimeter += 1
    elif (row, col-1) not in visited:
        group_cells.append((row, col-1))
    # right
    if col == len(map[row]) -1:
        perimeter += 1
    elif map[row][col+1] != map[row][col]:
        perimeter += 1
    elif (row, col+1) not in visited:
        group_cells.append((row, col+1))

    return perimeter

def get_price_of_group(map: List[str], row: int, col: int, visited: Set[Tuple[int, int]]) -> int:
    area = 1
    group_cells = []
    perimeter = get_perimeter_of_cell(map, row, col, group_cells, visited)
    while group_cells:
        next_cell = group_cells.pop()
        if next_cell not in visited:
            perimeter += get_perimeter_of_cell(map, next_cell[0], next_cell[1], group_cells, visited)
            area += 1
    # print("Found a group of {}. Area: {}, Perimeter: {}".format(map[row][col], area, perimeter))
    return area * perimeter

def get_price(map: [str]) -> int:
    price = 0
    visited = set()
    for row in range(len(map)):
        for col in range(len(map[row])):
            if (row, col) not in visited:
                price += get_price_of_group(map, row, col, visited)
    return price

if __name__=="__main__":
    input_file = open("input.txt", 'r')
    map = [line.strip() for line in input_file.readlines()]
    input_file.close()

    before = datetime.now()
    price = get_price(map)
    after = datetime.now()

    print("Part 1: {} ({})".format(price, after - before))