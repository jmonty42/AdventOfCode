from typing import Dict, List, Tuple, Set
from collections import defaultdict

def find_tower_locations(input_file_name: str) -> (Dict[str, List[Tuple[int, int]]], int, int):
    tower_locations = defaultdict(lambda: []) # frequency -> [(row, col)] - list of x,y pairs - want the order to stay the same for iterating

    input_file = open(input_file_name, 'r')
    lines = input_file.readlines()
    input_file.close()
    max_row = len(lines)-1
    max_col = len(lines[max_row])-1
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            frequency = lines[row][col]
            if frequency.isalnum():
                tower_locations[frequency].append((row, col))
    return tower_locations, max_row, max_col

def find_antinodes_for_two_towers(
        tower_1_location: Tuple[int, int],
        tower_2_location: Tuple[int, int]
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    diff_row = abs(tower_1_location[0] - tower_2_location[0])
    diff_col = abs(tower_1_location[1] - tower_2_location[1])
    antinode_near_tower_1_row = 0
    antinode_near_tower_1_col = 0
    antinode_near_tower_2_row = 0
    antinode_near_tower_2_col = 0
    if tower_1_location[0] < tower_2_location[0]:
        antinode_near_tower_1_row = tower_1_location[0] - diff_row
        antinode_near_tower_2_row = tower_2_location[0] + diff_row
    else:
        antinode_near_tower_1_row = tower_1_location[0] + diff_row
        antinode_near_tower_2_row = tower_2_location[0] - diff_row
    if tower_1_location[1] < tower_2_location[1]:
        antinode_near_tower_1_col = tower_1_location[1] - diff_col
        antinode_near_tower_2_col = tower_2_location[1] + diff_col
    else:
        antinode_near_tower_1_col = tower_1_location[1] + diff_col
        antinode_near_tower_2_col = tower_2_location[1] - diff_col
    return (
        (antinode_near_tower_1_row, antinode_near_tower_1_col),
        (antinode_near_tower_2_row, antinode_near_tower_2_col)
    )

def get_antinodes_in_range(
        tower_location: Tuple[int, int], diff_row: int, diff_col: int, max_row: int, max_col: int
) -> Set[Tuple[int,int]]:
    antinodes = set()
    new_antinode = (tower_location[0]+diff_row, tower_location[1]+diff_col)
    while 0 <= new_antinode[0] <= max_row and 0 <= new_antinode[1] <= max_col:
        antinodes.add(new_antinode)
        # print("Found antinode: {}".format(new_antinode))
        new_antinode = (new_antinode[0]+diff_row, new_antinode[1]+diff_col)
    # print("{} antinodes found here".format(len(antinodes)))
    return antinodes

def find_resonant_antinodes_in_range(
        tower_1_location: Tuple[int, int],
        tower_2_location: Tuple[int, int],
        max_row: int,
        max_col: int
) -> Set[Tuple[int, int]]:
    antinodes = set()
    diff_row = abs(tower_1_location[0] - tower_2_location[0])
    diff_col = abs(tower_1_location[1] - tower_2_location[1])
    if tower_1_location[0] < tower_2_location[0]:
        if tower_1_location[1] < tower_2_location[1]:
            antinodes = antinodes.union(get_antinodes_in_range(tower_1_location, -diff_row, -diff_col, max_row, max_col))
            antinodes = antinodes.union(get_antinodes_in_range(tower_2_location, diff_row, diff_col, max_row, max_col))
        else:
            antinodes = antinodes.union(get_antinodes_in_range(tower_1_location, -diff_row, diff_col, max_row, max_col))
            antinodes = antinodes.union(get_antinodes_in_range(tower_2_location, diff_row, -diff_col, max_row, max_col))
    else:
        if tower_1_location[1] < tower_2_location[1]:
            antinodes = antinodes.union(get_antinodes_in_range(tower_1_location, diff_row, -diff_col, max_row, max_col))
            antinodes = antinodes.union(get_antinodes_in_range(tower_2_location, -diff_row, diff_col, max_row, max_col))
        else:
            antinodes = antinodes.union(get_antinodes_in_range(tower_1_location, diff_row, diff_col, max_row, max_col))
            antinodes = antinodes.union(get_antinodes_in_range(tower_2_location, -diff_row, -diff_col, max_row, max_col))
    # print("in find_resonant_antinodes_in_range, found {} antinodes".format(len(antinodes)))
    return antinodes

def find_antinode_count(
        tower_locations: Dict[str, List[Tuple[int, int]]],
        max_row: int,
        max_col: int
) -> (int, int):
    antinode_locations: Set[Tuple[int, int]] = set()
    resonant_locations: Set[Tuple[int, int]] = set()
    for frequency in tower_locations:
        for first_tower_index in range(len(tower_locations[frequency])-1):
            for second_tower_index in range(first_tower_index+1, len(tower_locations[frequency])):
                # print("Finding antinodes for towers at {} and {} for frequency {}".format(
                #     tower_locations[frequency][first_tower_index],
                #     tower_locations[frequency][second_tower_index],
                #     frequency
                # ))
                antinodes = find_antinodes_for_two_towers(
                    tower_locations[frequency][first_tower_index],
                    tower_locations[frequency][second_tower_index]
                )
                for antinode in antinodes:
                    if 0 <= antinode[0] <= max_row and 0 <= antinode[1] <= max_col:
                        # print("\tFound one at {}".format(antinode))
                        antinode_locations.add(antinode)
                resonant_locations = resonant_locations.union(find_resonant_antinodes_in_range(
                    tower_locations[frequency][first_tower_index],
                    tower_locations[frequency][second_tower_index],
                    max_row,
                    max_col
                ))
                resonant_locations.add(tower_locations[frequency][first_tower_index])
                resonant_locations.add(tower_locations[frequency][second_tower_index])
    # print(str(antinode_locations))
    return len(antinode_locations), len(resonant_locations)

if __name__=="__main__":

    tower_locations, max_row, max_col = find_tower_locations("input.txt")
    part1_answer, part2_answer = find_antinode_count(tower_locations, max_row, max_col)
    print("Part 1: {}".format(part1_answer))
    print("Part 2: {}".format(part2_answer))
