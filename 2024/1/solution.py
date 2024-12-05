import heapq

input_file = open('input.txt', 'r')

left_list = []
right_list = []

for line in input_file:
    (left, right) = line.split()
    heapq.heappush(left_list, int(left)*-1)
    heapq.heappush(right_list, int(right)*-1)

input_file.close()

total_diff = 0

while left_list:
    left = heapq.heappop(left_list)
    right = heapq.heappop(right_list)
    total_diff += abs(left-right)

print(str(total_diff))

# part two
input_file = open('input.txt', 'r')

left_list = []
right_list = []

for line in input_file:
    (left, right) = line.split()
    left_list.append(int(left))
    right_list.append(int(right))

input_file.close()

similarity_score = 0

right_list_counts = {}

for number in right_list:
    if number in right_list_counts:
        right_list_counts[number] += 1
    else:
        right_list_counts[number] = 1

for number in left_list:
    if number in right_list_counts:
        similarity_score += number * right_list_counts[number]

print(str(similarity_score))