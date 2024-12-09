from datetime import datetime

def move_files_and_get_checksum(disk_map: str) -> int:
    debug_output = []
    sum = 0
    block_index = 0
    left_disk_index = 0
    right_disk_index = len(disk_map) - 1
    if right_disk_index % 2:
        # right index should always point to a file, so it must be even
        right_disk_index -= 1
    carryover_file_blocks = 0
    while right_disk_index > left_disk_index:
        # the right-most file can end up with the first of its blocks staying put while subsequent blocks get moved left
        # figure out what that means for right_disk_index and left_disk_index relation (probably check carryover after the loop
        if left_disk_index % 2:
            # index in disk map is odd, meaning we're pointing at free space
            free_blocks_to_fill = int(disk_map[left_disk_index])
            file_size_in_blocks = int(disk_map[right_disk_index])
            file_blocks_from_the_right = carryover_file_blocks if carryover_file_blocks > 0 else file_size_in_blocks
            file_id = right_disk_index // 2
            for block in range(free_blocks_to_fill):
                sum += block_index * file_id
                block_index += 1
                debug_output.append(file_id)
                file_blocks_from_the_right -= 1
                if file_blocks_from_the_right == 0:
                    # finished moving the current file, start pulling blocks from the next file to the left
                    right_disk_index -= 2
                    if right_disk_index < left_disk_index:
                        # we've filled all the empty space on the disk to the left of this block and no more files
                        # exist to the right
                        break
                    file_id = right_disk_index // 2
                    file_blocks_from_the_right = int(disk_map[right_disk_index])
            carryover_file_blocks = file_blocks_from_the_right
        else:
            # index in disk map is even, meaning we're pointing at a file
            file_size_in_blocks = int(disk_map[left_disk_index])
            file_id = left_disk_index // 2
            for block in range(file_size_in_blocks):
                sum += block_index * file_id
                block_index += 1
                debug_output.append(file_id)
        left_disk_index += 1
    if carryover_file_blocks:
        file_id = left_disk_index // 2
        for block in range(carryover_file_blocks):
            sum += block_index * file_id
            block_index += 1
            debug_output.append(file_id)
    # print("".join([str(file_id) for file_id in debug_output]))
    return sum

def move_file(blocks: [int], from_block: int, to_block: int):
    file_id = blocks[from_block]
    from_index = from_block
    to_index = to_block
    blocks_moved = 0
    while from_index < len(blocks) and blocks[from_index] == file_id:
        blocks[to_index] = file_id
        # doesn't matter what is put here as we move from right to left, so once a file is moved, nothing will be moved
        # into its place, just has to be a negative number
        blocks[from_index] = -1
        blocks_moved += 1
        from_index += 1
        to_index += 1
    if blocks[to_index] < 0: # negative number indicates free space
        # need to update the remaining free space with the correct size for future moves
        new_size = -blocks[to_index] - blocks_moved
        for _ in range(new_size):
            blocks[to_index] = -new_size
            to_index += 1


def move_whole_files_and_get_checksum(disk_map: str) -> int:
    blocks = [] # I'm pretty sure I will have to actually move things around before computing the checksum this time
    starting_block_for_file = []

    # build out the disk map
    for disk_index in range(len(disk_map)):
        size = int(disk_map[disk_index])
        if disk_index % 2:
            # index is odd, signifying free space
            for _ in range(size):
                blocks.append(-size) # negative size will signify a free space of `size` blocks
        else:
            # index is even, signifying a file
            file_id = disk_index // 2
            starting_block_for_file.append(len(blocks))
            for _ in range(size):
                blocks.append(file_id)
    # print(str(starting_block_for_file))
    # print("".join([str(block) if block >= 0 else '.' for block in blocks]))

    sum = 0

    right_file_index = len(disk_map) - 1
    if right_file_index % 2:
        right_file_index -= 1

    while right_file_index >= 0:
        file_id = right_file_index // 2
        file_size = int(disk_map[right_file_index])
        for block_index in range(len(blocks)):
            if blocks[block_index] < 0:
                free_blocks = -blocks[block_index]
                if free_blocks >= file_size:
                    move_file(blocks, starting_block_for_file[file_id], block_index)
                    for _ in range(file_size):
                        sum += block_index * file_id
                        block_index += 1
                    break
            elif blocks[block_index] == file_id:
                for _ in range(file_size):
                    sum += block_index * file_id
                    block_index += 1
                break
        right_file_index -= 2

    # print("".join([str(block) if block >= 0 else '.' for block in blocks]))

    return sum

if __name__=="__main__":
    input_file = open("input.txt", 'r')
    disk_map = input_file.readline()
    input_file.close()
    before = datetime.now()
    checksum_part_1 = move_files_and_get_checksum(disk_map)
    after = datetime.now()
    print("Part 1: {} ({})".format(checksum_part_1, after-before))
    before = datetime.now()
    checksum_part_2 = move_whole_files_and_get_checksum(disk_map)
    after = datetime.now()
    print("Part 2: {} ({})".format(checksum_part_2, after-before))