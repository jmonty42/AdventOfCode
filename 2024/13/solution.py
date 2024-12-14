import math
import re
from datetime import datetime
from typing import List, Tuple

def find_min_price_for_machine(machine: Tuple[Tuple[int, int],Tuple[int, int],Tuple[int, int]]) -> int:
    min_cost = 0
    button_a_x = machine[0][0]
    button_a_y = machine[0][1]
    button_b_x = machine[1][0]
    button_b_y = machine[1][1]
    prize_x = machine[2][0]
    prize_y = machine[2][1]
    for button_a_presses in range(1,101):
        dif_x = prize_x - (button_a_x * button_a_presses)
        if dif_x % button_b_x == 0 \
            and (button_a_y * button_a_presses) + (button_b_y * (dif_x//button_b_x)) == prize_y:
            cost = (button_a_presses * 3) + (dif_x//button_b_x)
            if min_cost == 0 or cost < min_cost:
                min_cost = cost
    return min_cost

def find_min_price(machines: List[Tuple[Tuple[int, int],Tuple[int, int],Tuple[int, int]]]) -> int:
    cost = 0
    for machine in machines:
        cost += find_min_price_for_machine(machine)
    return cost

if __name__=="__main__":
    before = datetime.now()
    input_file = open("input.txt", 'r')
    line = input_file.readline()
    machines = []
    a_pattern = re.compile(r"Button A: X\+(\d+), Y\+(\d+)")
    b_pattern = re.compile(r"Button B: X\+(\d+), Y\+(\d+)")
    prize_pattern = re.compile(r"Prize: X=(\d+), Y=(\d+)")
    while line:
        a_match = a_pattern.match(line)
        b_match = b_pattern.match(line)
        prize_match = prize_pattern.match(line)
        if a_match:
            a_button = int(a_match.group(1)), int(a_match.group(2))
        elif b_match:
            b_button = int(b_match.group(1)), int(b_match.group(2))
        elif prize_match:
            machines.append((
                a_button,
                b_button,
                (int(prize_match.group(1)), int(prize_match.group(2)))
            ))
        line = input_file.readline()
    input_file.close()
    after = datetime.now()

    print("Setup: {}".format(after - before))

    before = datetime.now()
    min_price = find_min_price(machines)
    after = datetime.now()
    print("Part 1: {} ({})".format(min_price, after - before))