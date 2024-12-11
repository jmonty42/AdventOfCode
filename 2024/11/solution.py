from datetime import datetime
from typing import List

def blink(stones: [int]) -> List[int]:
    new_stones_list = []
    for stone in stones:
        if stone == 0:
            new_stones_list.append(1)
        elif len(str(stone)) % 2 == 0:
            mid = len(str(stone)) // 2
            new_stones_list.append(int(str(stone)[:mid]))
            new_stones_list.append(int(str(stone)[mid:]))
        else:
            new_stones_list.append(stone*2024)
    return new_stones_list

def blink_25(stones: [int]) -> int:
    for _ in range(25):
        stones = blink(stones)
    return len(stones)

if __name__=="__main__":
    input_file = open("input.txt", 'r')
    stones = [int(stone) for stone in input_file.readline().split()]
    input_file.close()

    before = datetime.now()
    stone_count = blink_25(stones)
    after = datetime.now()
    print("Part 1: {} ({})".format(stone_count, after - before))