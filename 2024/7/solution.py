
def is_result_possible(numbers: [int], result: int, running_result: int) -> bool:
    if len(numbers) == 1:
        return running_result + numbers[0] == result or running_result * numbers[0] == result
    next_result = running_result + numbers[0]
    if is_result_possible(numbers[1:], result, next_result):
        return True
    next_result = running_result * numbers[0]
    return is_result_possible(numbers[1:], result, next_result)

def try_concatenation(numbers: [int], result: int, running_result: int) -> bool:
    if len(numbers) == 1:
        return running_result + numbers[0] == result or running_result * numbers[0] == result or \
            int(str(running_result)+str(numbers[0])) == result
    next_result = running_result + numbers[0]
    if try_concatenation(numbers[1:], result, next_result):
        return True
    next_result = running_result * numbers[0]
    if try_concatenation(numbers[1:], result, next_result):
        return True
    next_result = int(str(running_result)+str(numbers[0]))
    return try_concatenation(numbers[1:], result, next_result)

input_file = open('input.txt', 'r')

sum = 0
part_2_sum = 0

for line in input_file.readlines():
    number_strings = line.split()
    result = int(number_strings[0][:-1])
    numbers = [int(x) for x in number_strings[1:]]
    if is_result_possible(numbers[1:], result, numbers[0]):
        # print("{} is valid with only addition and multiplication.".format(line.strip()))
        sum += result
        part_2_sum += result
    elif try_concatenation(numbers[1:], result, numbers[0]):
        part_2_sum += result

input_file.close()

print("Part 1: {}".format(sum))
print("Part 2: {}".format(part_2_sum))