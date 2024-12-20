from datetime import datetime

CARDINAL_DIRECTIONS = [(-1,0), (0, 1), (1, 0), (0, -1)]

def find_score_of_trailhead(map: [[int|str]], row: int, col: int, rating=False) -> int:
    score = 0
    cells_visited = set()
    neighbors_to_walk = [(row, col)]

    while neighbors_to_walk:
        current_cell = neighbors_to_walk.pop()
        if current_cell not in cells_visited or rating:
            cells_visited.add(current_cell)
            if map[current_cell[0]][current_cell[1]] == 9:
                score += 1
            else:
                for direction in CARDINAL_DIRECTIONS:
                    neighbor = (current_cell[0]+direction[0], current_cell[1]+direction[1])
                    if 0 <= neighbor[0] < len(map) \
                        and 0 <= neighbor[1] < len(map[neighbor[0]]) \
                        and (neighbor not in cells_visited or rating) \
                        and type(map[neighbor[0]][neighbor[1]]) == int \
                        and map[neighbor[0]][neighbor[1]] - map[current_cell[0]][current_cell[1]] == 1:
                            neighbors_to_walk.append(neighbor)

    return score

def sum_of_trailhead_scores(map: [[int|str]], rating=False) -> int:
    total_score = 0
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == 0:
                total_score += find_score_of_trailhead(map, row, col, rating)
    return total_score

if __name__ == "__main__":
    input_file = open("input.txt", 'r')
    map_as_ints = [[int(character) if character.isdigit() else character for character in line] for line in input_file.readlines()]
    input_file.close()
    before = datetime.now()
    part_1_answer = sum_of_trailhead_scores(map_as_ints)
    after = datetime.now()
    print("Part 1: {} ({})".format(part_1_answer, after - before))
    before = datetime.now()
    part_2_answer = sum_of_trailhead_scores(map_as_ints, rating=True)
    after = datetime.now()
    print("Part 2: {} ({})".format(part_2_answer, after - before))