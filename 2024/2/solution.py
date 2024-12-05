from typing import List

input_file = open('input.txt', 'r')

def is_report_safe(levels: List[int]) -> bool:
    increasing = levels[0] < levels[1]
    safe = True
    for index in range(1,len(levels)):
        if (levels[index-1] < levels[index] and increasing) or (levels[index-1] > levels[index] and not increasing):
            if abs(levels[index]-levels[index-1]) >= 4:
                safe = False
                break
        else:
            safe = False
            break
    return safe

total_safe = 0

for line in input_file:
    levels = [int(s) for s in line.split()]
    safe = is_report_safe(levels)
    if safe:
        total_safe += 1
    # do this for part 2:
    # This part was tricky because being able to skip one level in a report made it difficult to determine
    # if the trend was increasing or decreasing, so I just brute forced it
    else:
        for skip in range(len(levels)+1):
            safe = is_report_safe(levels[0:skip]+levels[skip+1:len(levels)+1])
            if safe:
                total_safe += 1
                break

    # print("{}: {}".format(levels, safe))


print(str(total_safe))
