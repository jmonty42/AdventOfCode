from datetime import datetime
from typing import List, Dict

def blink(stone: int, iterations: Dict[int, List[List[int]]]) -> List[int]:
    if stone not in iterations:
        new_stones_list = []

        if stone == 0:
            new_stones_list.append(1)
        elif len(str(stone)) % 2 == 0:
            mid = len(str(stone)) // 2
            new_stones_list.append(int(str(stone)[:mid]))
            new_stones_list.append(int(str(stone)[mid:]))
        else:
            new_stones_list.append(stone*2024)

        iterations[stone] = [new_stones_list]

    return iterations[stone][0]

def continue_iterating_on_stone(stone: int, n: int, iterations: Dict[int, List[List[int]]]):
    for iteration in range(len(iterations[stone]), n):
        this_iteration_stone_list = []
        for old_stone in iterations[stone][iteration - 1]:
            blink_n_times(old_stone, n - iteration, iterations)
            this_iteration_stone_list += iterations[old_stone][0]
        if iteration == len(iterations[stone]):
            iterations[stone].append(this_iteration_stone_list)

def blink_n_times(stone: int, n: int, iterations: Dict[int, List[List[int]]]) -> int:
    if stone not in iterations:
        iterations[stone] = [blink(stone, iterations)]
    if len(iterations[stone]) < n:
        continue_iterating_on_stone(stone, n, iterations)

    return len(iterations[stone][n-1])

def blink_n(stones: [int], n: int) -> int:
    count = 0
    iterations = {} # starting value -> [] result after n+1 iterations
    for stone in stones:
        count += blink_n_times(stone, n, iterations)
    return count

if __name__=="__main__":
    input_file = open("input.txt", 'r')
    stones = [int(stone) for stone in input_file.readline().split()]
    input_file.close()

    before = datetime.now()
    stone_count = blink_n(stones, 25)
    after = datetime.now()
    print("Part 1: {} ({})".format(stone_count, after - before))

    before = datetime.now()
    stone_count = blink_n(stones, 75)
    after = datetime.now()
    print("Part 2: {} ({})".format(stone_count, after - before))