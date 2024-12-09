
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
    print("".join([str(file_id) for file_id in debug_output]))
    return sum

if __name__=="__main__":
    input_file = open("input.txt", 'r')
    disk_map = input_file.readline()
    input_file.close()
    print("Part 1: {}".format(move_files_and_get_checksum(disk_map)))