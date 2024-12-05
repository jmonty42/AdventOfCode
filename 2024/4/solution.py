from enum import Enum

class Direction(Enum):
    BACKWARDS = 1
    FORWARDS = 2
    UP = 3
    DOWN = 4
    UP_LEFT = 5
    UP_RIGHT = 6
    DOWN_LEFT = 7
    DOWN_RIGHT = 8

def next_cell_in_direction(row: int, col: int, direction:Direction) -> (int, int):
    next_row = row
    next_col = col
    if direction in [Direction.UP, Direction.UP_LEFT, Direction.UP_RIGHT]:
        next_row -= 1
    elif direction in [Direction.DOWN, Direction.DOWN_LEFT, Direction.DOWN_RIGHT]:
        next_row += 1
    if direction in [Direction.BACKWARDS, Direction.UP_LEFT, Direction.DOWN_LEFT]:
        next_col -= 1
    elif direction in [Direction.FORWARDS, Direction.UP_RIGHT, Direction.DOWN_RIGHT]:
        next_col += 1
    return next_row, next_col

def count_at_location(wordsearch: [str], row: int, col: int) -> int:
    keyword = "XMAS"
    count = 0
    for direction in Direction:
        keyword_index = 0
        searching_row = row
        searching_col = col
        found = False
        while keyword_index < len(keyword) and \
                0 <= searching_row < len(wordsearch) and \
                0 <= searching_col < len(wordsearch[searching_row]) and \
                wordsearch[searching_row][searching_col] == keyword[keyword_index]:
            if keyword_index == len(keyword) - 1:
                found = True
                break
            searching_row, searching_col = next_cell_in_direction(searching_row, searching_col, direction)
            keyword_index += 1
        if found:
            count += 1
    return count

def find_x_of_mas(wordsearch: [str], row: int, col: int) -> bool:
    # row and col cannot be on the edge:
    if row <= 0 or row >= len(wordsearch)-1:
        return False
    if col <= 0 or col >= len(wordsearch[row])-1:
        return False
    if wordsearch[row][col] == 'A':
        top_left = next_cell_in_direction(row, col, Direction.UP_LEFT)
        top_right = next_cell_in_direction(row, col, Direction.UP_RIGHT)
        bottom_left = next_cell_in_direction(row, col, Direction.DOWN_LEFT)
        bottom_right = next_cell_in_direction(row, col, Direction.DOWN_RIGHT)
        if (wordsearch[top_left[0]][top_left[1]] == 'M' or wordsearch[top_left[0]][top_left[1]] == 'S') and \
            (wordsearch[bottom_right[0]][bottom_right[1]] == 'M' or wordsearch[bottom_right[0]][bottom_right[1]] == 'S') and \
            wordsearch[top_left[0]][top_left[1]] != wordsearch[bottom_right[0]][bottom_right[1]]:
            # one 'MAS' found
            if (wordsearch[top_right[0]][top_right[1]] == 'M' or wordsearch[top_right[0]][top_right[1]] == 'S') and \
                (wordsearch[bottom_left[0]][bottom_left[1]] == 'M' or wordsearch[bottom_left[0]][bottom_left[1]] == 'S') and \
                wordsearch[top_right[0]][top_right[1]] != wordsearch[bottom_left[0]][bottom_left[1]]:
                # other 'MAS' found
                # print("X-MAS found at ({},{})".format(row, col))
                return True
    return False

input_file = open('input.txt', 'r')

wordsearch = input_file.readlines()

input_file.close()

words_found = 0
x_of_mas_found = 0

for row in range(len(wordsearch)):
    for col in range(len(wordsearch[row])):
        words_found += count_at_location(wordsearch, row, col)
        if find_x_of_mas(wordsearch, row, col):
            x_of_mas_found += 1

print("Solution to part1: {}".format(words_found))
print("Solution to part2: {}".format(x_of_mas_found))

