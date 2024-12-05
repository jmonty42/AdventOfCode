import re

input_file = open('input.txt', 'r')

sum = 0
do = True

for line in input_file:
    matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))", line)
    for match in matches:
        if not match[2] and not match[3] and do:
            sum += int(match[0]) * int(match[1])
        elif match[2] == 'do()':
            do = True
        elif match[3] == "don't()":
            do = False

print(str(sum))
