import re
from typing import List, Tuple

def get_safety_factor(robots: List[Tuple[Tuple[int, int],Tuple[int, int]]], width: int, height : int) -> int:
    robots_in_quadrant = [0, 0, 0, 0]
    for robot in robots:
        starting_x = robot[0][0]
        starting_y = robot[0][1]
        speed_x = robot[1][0]
        speed_y = robot[1][1]
        new_x = (starting_x + (speed_x * 100)) % width
        new_y = (starting_y + (speed_y * 100)) % height
        if new_x < width // 2:
            if new_y < height // 2:
                robots_in_quadrant[0] += 1
            elif new_y > height // 2:
                robots_in_quadrant[1] += 1
        elif new_x > width // 2:
            if new_y < height // 2:
                robots_in_quadrant[2] += 1
            elif new_y > height // 2:
                robots_in_quadrant[3] += 1
    return robots_in_quadrant[0] * robots_in_quadrant[1] * robots_in_quadrant[2] * robots_in_quadrant[3]

if __name__ == "__main__":
    input_file = open("input.txt", 'r')
    width = int(input_file.readline().strip())
    height = int(input_file.readline().strip())
    robots = []
    pattern = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")
    for line in input_file.readlines():
        match = pattern.match(line)
        if match:
            robots.append((
                (int(match.group(1)),int(match.group(2))),
                (int(match.group(3)),int(match.group(4)))
            ))

    print(str(get_safety_factor(
        robots,
        width,
        height
    )))