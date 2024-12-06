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

def mark_intercept_path(row: int, col: int, new_direction: Direction,
                        map: [str], intercepts: [[Set[Direction]]], possible_obstacle_locations: Set[Tuple[int, int]],
                        visited: [[Set[Direction]]]):
    # at a cell where you turn to the right, any cells to the left become potential paths to take to create a loop
    # as in, if you pass through a cell to the left of this cell you just turned to (to the left stopping at a current obstacle)
    # you would wind up back on this cell going in the direction you've already gone
    opposite_direction = turn_right(turn_right(new_direction))
    prev_row, prev_col = next_cell_in_direction((row, col), opposite_direction)
    # Additionally, any obstacle that is to the right of a cell on this path (when traveling in `opposite_direction`)
    # creates another potential intercept path
    while 0 <= prev_row < len(map) and 0 <= prev_col < len(map[prev_row]):
        if map[prev_row][prev_col] == '#' or new_direction in intercepts[prev_row][prev_col]:
            break
        intercepts[prev_row][prev_col].add(new_direction)
        right = turn_right(opposite_direction)
        # if we've previously traversed this cell going to the right, we've found another possible location
        if right in visited[prev_row][prev_col]:
            next_row, next_col = next_cell_in_direction((prev_row,prev_col),right)
            if 0 <= next_row < len(map) and 0 <= next_col < len(map[next_row]):
                possible_obstacle_locations.add((next_row, next_col))
        # if the cell to the right of (prev_row, prev_col) is an obstacle, mark that path as well
        right_row, right_col = next_cell_in_direction((prev_row, prev_col), right)
        if 0 <= right_row < len(map) and 0 <= right_col < len(map[right_row]) and \
            map[right_row][right_col] == '#':
            mark_intercept_path(right_row, right_col, right, map, intercepts, possible_obstacle_locations, visited)
        prev_row, prev_col = next_cell_in_direction((prev_row, prev_col), opposite_direction)

input_file = open('example.txt', 'r')

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

# every time we change direction, we have to populate cells in the opposite direction as potential intercept paths
intercept_directions = []
for row in range(len(map)):
    intercept_directions.append([])
    for col in range(len(map[row])):
        intercept_directions[row].append(set())

exited = False
direction = Direction.UP
row = starting_location[0]
col = starting_location[1]

possible_obstacle_locations = set()

mark_intercept_path(row, col, direction, map, intercept_directions, possible_obstacle_locations, visited)

while not exited:
    # print("At {},{}, we're going {}".format(row, col, direction))
    visited[row][col].add(direction) # log the direction we are traveling in the current cell
    # if on our path we cross a cell where we previously traveled to the right, we've found a place we can make a loop
    to_the_right = turn_right(direction)
    if to_the_right in visited[row][col]:
        print("At {},{} we've previously gone to the right ({})".format(row,col,to_the_right))
        possible_obstacle_locations.add(next_cell_in_direction((row,col),direction))
        print("Placing obstacle at {}".format(next_cell_in_direction((row, col),direction)))
    # if turning to the right at our current location would intercept our previous path, it's another possible obstacle location
    elif to_the_right in intercept_directions[row][col]:
        print("If we turned right ({}) at {},{}, we'd intercept part of our original path.".format(to_the_right, row, col))
        possible_obstacle_locations.add(next_cell_in_direction((row, col), direction))
        print("Placing obstacle at {}".format(next_cell_in_direction((row, col),direction)))
    next_row, next_col = next_cell_in_direction((row, col), direction)
    if next_row < 0 or next_row >= len(map) or next_col < 0 or next_col >= len(map[0]):
        exited = True
    elif map[next_row][next_col] == '#':
        direction = turn_right(direction)
        mark_intercept_path(row, col, direction, map, intercept_directions, possible_obstacle_locations, visited)
    else:
        if not visited[next_row][next_col]:
            visited_count += 1
            map[next_row] = map[next_row][:next_col] + 'X' + map[next_row][next_col+1:]
        row = next_row
        col = next_col

if starting_location in possible_obstacle_locations:
    print("Removing the starting location as a possible obstacle location.")
    possible_obstacle_locations.remove(starting_location)

output_file = open('example-output.txt', 'w')

print(str(starting_location))
for row in map:
    output_file.write(row)
print("Part 1: {}".format(visited_count))
print("Part 2: {}".format(len(possible_obstacle_locations)))
print("{}".format(possible_obstacle_locations))