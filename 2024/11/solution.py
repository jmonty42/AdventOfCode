from datetime import datetime
from typing import List, Dict
from collections import defaultdict

def blink(stone_counts: Dict[int, int]) -> Dict[int, int]:
    new_stone_counts: Dict[int, int] = defaultdict(int)
    for stone in stone_counts:
        if stone == 0:
            new_stone_counts[1] += stone_counts[0]
        elif len(str(stone)) % 2 == 0:
            mid = len(str(stone)) // 2
            new_stone_counts[int(str(stone)[:mid])] += stone_counts[stone]
            new_stone_counts[int(str(stone)[mid:])] += stone_counts[stone]
        else:
            new_stone_counts[stone*2024] += stone_counts[stone]

    return new_stone_counts

def blink_list_n_times(stones: List[int], n: int) -> int:
    stone_counts: Dict[int, int] = defaultdict(int)
    for stone in stones:
        stone_counts[stone] += 1

    for _ in range(n):
        stone_counts = blink(stone_counts)

    total_stones = 0
    for stone in stone_counts:
        total_stones += stone_counts[stone]

    return total_stones

if __name__=="__main__":
    input_file = open("input.txt", 'r')
    stones = [int(stone) for stone in input_file.readline().split()]
    input_file.close()

    before = datetime.now()
    part_1_answer = blink_list_n_times(stones, 25)
    after = datetime.now()
    print("Part 1: {} ({})".format(part_1_answer, after - before))

    before = datetime.now()
    part_2_answer = blink_list_n_times(stones, 75)
    after = datetime.now()
    print("Part 2: {} ({})".format(part_2_answer, after - before))