from datetime import datetime
from typing import Set, List, Tuple

def get_corners_of_cell(
        map: List[str], row: int, col: int, group_cells: List[Tuple[int, int]], visited: Set[Tuple[int, int]]) -> int:
    corners: Set[Tuple[int, int]] = set()
    directions = [
        (-1, -1), # NW
        (-1, 1),  # NE
        (1, 1),   # SE
        (1, -1)   # SW
    ]
    group = map[row][col]
    for direction in directions:
        # check for 90° corner
        if (row == 0 and col == 0 and direction == (-1,-1)) \
            or (row == 0 and col == len(map[row])-1 and direction == (-1, 1)) \
            or (row == len(map)-1 and col == 0 and direction == (1, -1)) \
            or (row == len(map)-1 and col == len(map[row])-1 and direction == (1,1)):
            corners.add(
                (row + direction[0] if direction[0] > 0 else row, col + direction[1] if direction[1] > 0 else col)
            )
        # for the top and bottom rows, a corner exists if the singular neighbor in direction is different
        elif ((row == 0 and (direction == (-1, -1) or direction == (-1, 1)))
            or (row == len(map)-1 and (direction == (1, 1) or direction == (1, -1)))) \
            and map[row][col+direction[1]] != group:
            corners.add(
                (row + direction[0] if direction[0] > 0 else row, col + direction[1] if direction[1] > 0 else col)
            )
        # for the left and right cols, a corner exists if the singular neighbor in direction is different
        elif ((col == 0 and (direction == (-1, -1) or direction == (1, -1)))
            or (col == len(map[row])-1) and (direction == (-1, 1) or direction == (1, 1))) \
            and map[row+direction[0]][col] != group:
            corners.add(
                (row + direction[0] if direction[0] > 0 else row, col + direction[1] if direction[1] > 0 else col)
            )
        elif (0 <= col+direction[1] < len(map[row]) and map[row][col+direction[1]] != group) \
                and (0<= row+direction[0] < len(map) and map[row+direction[0]][col] != group):
            corners.add(
                (row + direction[0] if direction[0] > 0 else row, col + direction[1] if direction[1] > 0 else col)
            )
        # check for 270° corner
        elif (0 <= col+direction[1] < len(map[row]) and map[row][col+direction[1]] == group) \
                and (0<= row+direction[0] < len(map) and map[row+direction[0]][col] == group) \
                and (0 <= col+direction[1] < len(map[row]) and 0<= row+direction[0] < len(map)
                     and map[row+direction[0]][col+direction[1]] != group):
            corners.add(
                (row + direction[0] if direction[0] > 0 else row, col + direction[1] if direction[1] > 0 else col)
            )
        if 0 <= col+direction[1] < len(map[row]) and map[row][col+direction[1]] == group \
                and (row, col+direction[1]) not in visited:
            group_cells.append((row, col+direction[1]))
        if 0 <= row+direction[0] < len(map) and map[row+direction[0]][col] == group \
                and (row+direction[0], col) not in visited:
            group_cells.append((row+direction[0], col))

    return len(corners)

def get_perimeter_or_corners_of_cell(
        map: List[str], row: int, col: int, group_cells: List[Tuple[int, int]], visited: Set[Tuple[int,int]],
        corners: bool=False) -> int:
    visited.add((row, col))
    if corners:
        return get_corners_of_cell(map, row, col, group_cells, visited)
    perimeter = 0
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

def get_price_of_group(map: List[str], row: int, col: int, visited: Set[Tuple[int, int]], by_side: bool=False) -> int:
    area = 1
    group_cells = []
    perimeter_or_corners = get_perimeter_or_corners_of_cell(map, row, col, group_cells, visited, by_side)
    while group_cells:
        next_cell = group_cells.pop()
        if next_cell not in visited:
            perimeter_or_corners += get_perimeter_or_corners_of_cell(
                map, next_cell[0], next_cell[1], group_cells, visited, by_side)
            area += 1
    # print("Found a group of {}. Area: {}, Perimeter: {}".format(map[row][col], area, perimeter))
    return area * perimeter_or_corners

def get_price(map: [str], by_side: bool=False) -> int:
    price = 0
    visited = set()
    for row in range(len(map)):
        for col in range(len(map[row])):
            if (row, col) not in visited:
                price += get_price_of_group(map, row, col, visited, by_side)
    return price

if __name__=="__main__":
    input_file = open("input.txt", 'r')
    map = [line.strip() for line in input_file.readlines()]
    input_file.close()

    before = datetime.now()
    price = get_price(map)
    after = datetime.now()

    print("Part 1: {} ({})".format(price, after - before))

    before = datetime.now()
    price = get_price(map, True)
    after = datetime.now()

    print("Part 2: {} ({})".format(price, after - before))