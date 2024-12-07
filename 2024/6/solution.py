from enum import Enum
from typing import Set, Tuple

class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

def turn_right(direction: Direction) -> Direction:
    if direction == Direction.UP:
        return Direction.RIGHT
    if direction == Direction.RIGHT:
        return Direction.DOWN
    if direction == Direction.DOWN:
        return Direction.LEFT
    return Direction.UP

def next_cell_in_direction(current_cell: (int, int), direction: Direction) -> (int, int):
    if direction == Direction.UP:
        return current_cell[0]-1, current_cell[1]
    if direction == Direction.RIGHT:
        return current_cell[0], current_cell[1]+1
    if direction == Direction.DOWN:
        return current_cell[0]+1, current_cell[1]
    return current_cell[0], current_cell[1]-1

def test_if_an_obstacle_would_create_a_loop(start_row: int, start_col: int, start_direction: Direction, map: [str],
                                            visited: [[Set[Direction]]]) -> bool:
    row, col, direction = start_row, start_col, start_direction
    # from a given position and facing direction, would placing an obstacle in the next cell in that direction result in a loop?
    next_row, next_col = next_cell_in_direction((row, col), direction)
    if next_row < 0 or next_row >= len(map) or next_col < 0 or next_col >= len(map[next_row]):
        # you can't place an obstacle outside the map, so it wouldn't create a loop
        return False
    old_cell_value = map[next_row][next_col]
    map[next_row] = map[next_row][:next_col] + '#' + map[next_row][next_col + 1:]
    direction = turn_right(direction)
    temp_visited = []
    for r in range(len(map)):
        temp_visited.append([])
        for c in range(len(map[r])):
            temp_visited[r].append(set())
    exited = False
    loop = False
    while not exited and not loop:
        temp_visited[row][col].add(direction)
        next_row, next_col = next_cell_in_direction((row, col), direction)
        if next_row < 0 or next_row >= len(map) or next_col < 0 or next_col >= len(map[next_row]):
            exited = True
        elif map[next_row][next_col] == '#':
            direction = turn_right(direction)
        elif direction in visited[next_row][next_col] or direction in temp_visited[next_row][next_col]:
            loop = True
        else:
            row = next_row
            col = next_col
    next_row, next_col = next_cell_in_direction((start_row, start_col), start_direction)
    map[next_row] = map[next_row][:next_col] + old_cell_value + map[next_row][next_col + 1:]
    return loop

input_file = open('input.txt', 'r')

map = input_file.readlines()

input_file.close()

starting_location = None

for row in range(len(map)):
    if '^' in map[row]:
        col = map[row].find('^')
        starting_location = (row, col)
        break

visited = []
for row in range(len(map)):
    visited.append([])
    for col in range(len(map[row])):
        visited[row].append(set())
visited_count = 1

row = starting_location[0]
col = starting_location[1]

exited = False
direction = Direction.UP

possible_obstacle_locations = set()

while not exited:
    # print("At {},{}, we're going {}".format(row, col, direction))
    visited[row][col].add(direction) # log the direction we are traveling in the current cell
    next_row, next_col = next_cell_in_direction((row, col), direction)
    if next_row < 0 or next_row >= len(map) or next_col < 0 or next_col >= len(map[0]):
        exited = True
    elif map[next_row][next_col] == '#':
        direction = turn_right(direction)
    else:
        if not visited[next_row][next_col]:
            # test if placing an obstacle in the next cell would create a loop
            if test_if_an_obstacle_would_create_a_loop(row, col, direction, map, visited):
                possible_obstacle_locations.add((next_row, next_col))
            visited_count += 1
            map[next_row] = map[next_row][:next_col] + 'X' + map[next_row][next_col+1:]
        row = next_row
        col = next_col

if starting_location in possible_obstacle_locations:
    print("Removing the starting location as a possible obstacle location.")
    possible_obstacle_locations.remove(starting_location)

output_file = open('output.txt', 'w')

# print(str(starting_location))
for row in map:
    output_file.write(row)
print("Part 1: {}".format(visited_count))
print("Part 2: {}".format(len(possible_obstacle_locations)))
# print("{}".format(possible_obstacle_locations))