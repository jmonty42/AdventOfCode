
input_file = open('input.txt', 'r')

page_dependencies = {} # page -> {pages it must be before}
reverse_page_dependencies = {} # page -> {pages it must be after}

sum = 0
corrected_sum = 0

def check_correct_order(pages: [int]) -> bool:
    pages_seen = set()
    for current_page in pages:
        for previous_page in pages_seen:
            if current_page in page_dependencies and previous_page in page_dependencies[current_page]:
                return False
        pages_seen.add(current_page)
    return True

def reorder_and_get_mid_page(pages: [int]) -> int:
    while not check_correct_order(pages):
        pages_seen = {} # page -> index
        swapped = False
        for page_index in range(len(pages)):
            current_page = pages[page_index]
            for previous_page in pages_seen:
                if current_page in page_dependencies and previous_page in page_dependencies[current_page]:
                    swapped = True
                    pages[page_index] = previous_page
                    pages[pages_seen[previous_page]] = current_page
                    break
            if not swapped:
                pages_seen[current_page] = page_index
            else:
                break
    return int(pages[len(pages)//2])

for line in input_file.readlines():
    if '|' in line:
        pages = [int(num) for num in line.split('|')]
        if pages[0] not in page_dependencies:
            page_dependencies[pages[0]] = set()
        page_dependencies[pages[0]].add(pages[1])
        if pages[1] not in reverse_page_dependencies:
            reverse_page_dependencies[pages[1]] = set()
        reverse_page_dependencies[pages[1]].add(pages[0])
    elif ',' in line:
        pages = [int(num) for num in line.split(',')]
        valid = check_correct_order(pages)
        if valid:
            mid = len(pages) // 2
            sum += pages[mid]
        else:
            corrected_sum += reorder_and_get_mid_page(pages)

print("Part 1: {}".format(sum))
print("Part 2: {}".format(corrected_sum))