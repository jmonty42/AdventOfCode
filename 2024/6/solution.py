from enum import Enum

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

input_file = open('example.txt', 'r')

map = input_file.readlines()

input_file.close()

starting_location = None

for row in range(len(map)):
    if '^' in map[row]:
        col = map[row].find('^')
        starting_location = (row, col)
        break

visited = [[False]*len(map[0]) for i in range(len(map))]
visited[starting_location[0]][starting_location[1]] = True
visited_count = 1

exited = False
direction = Direction.UP
row = starting_location[0]
col = starting_location[1]

while not exited:
    next_row, next_col = next_cell_in_direction((row, col), direction)
    if next_row < 0 or next_row >= len(map) or next_col < 0 or next_col >= len(map[0]):
        exited = True
    elif map[next_row][next_col] == '#':
        direction = turn_right(direction)
    else:
        if not visited[next_row][next_col]:
            visited[next_row][next_col] = True
            visited_count += 1
            map[next_row] = map[next_row][:next_col] + 'X' + map[next_row][next_col+1:]
        row = next_row
        col = next_col

output_file = open('example-output.txt', 'w')

print(str(starting_location))
for row in map:
    output_file.write(row)
print("Part 1: {}".format(visited_count))