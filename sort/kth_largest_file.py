"""
Get the kth largest integer from a file

Why this works.
Each chunk can fit in memory
We sort each chunk
so smallest value on left, largest value on right
when we get to kth index, it is the kth largest of that chunk

Use min-heap as consolidator
add all first / smallest elements from every chunk

we pop the heap to get the smallest
we replace the value from the same chunk
 - this ensures we are reading from all chunks

When we read k elements, it is the kth largest from all of the 
numbers read
BECAUSE
  we already read them into the chunks

So the kth read from min-heap is the kth largest
"""

from heapq import heapify, heappush, heappop
import os

def find_kth_largest(filename, k):
    # split file into chunks, sort each chunk, save to disk
    chunk_size = 100000
    chunk_filenames = []
    chunk_number = 0

    # open the original file
    with open(filename, 'r') as file:
        # loop forever
        while True:

            # read up to memory size of integers from file
            chunk = []
            for _ in range(chunk_size):
                line = file.readline()
                if line:
                    chunk.append(int(line.strip()))
                else:
                    break
            
            # after finished reading
            if chunk:
                # sort the individual chunk
                chunk.sort()

                # write sorted chunk to new file
                chunk_filename = f"chunk_{chunk_number}.txt"
                with open(chunk_filename, 'w') as chunk_file:
                    for num in chunk:
                        chunk_file.write(f"{num}\n")

                # keep track of files
                chunk_filenames.append(chunk_filename)
                # increment filename
                chunk_number += 1
            else:
                # cannot read anymore
                break

    # Use min-heap for all the sorted chunks
    min_heap = []
    file_handlers = []

    # open all created files and save in list
    for chunk_filename in chunk_filenames:
        file_handlers.append(open(chunk_filename, 'r'))

    # initialize heap with first element of all chunks
    for i, file_handler in enumerate(file_handlers):
        line = file_handler.readline()
        if line:
            # push a tuple of value, index
            val = int(line.strip())
            heappush(min_heap, (val, i))

    count = 0
    kth_largest = None

    while min_heap:
        # pop smallest element
        val, chunk_index = heappop(min_heap)
        count += 1

        # if we see k, we are done
        if count == k:
            kth_largest = val
            break
        
        # read next element from same chunk
        # this is because we are replacing the element we removed
        line = file_handlers[chunk_index].readline()
        if line:
            val = int(line.strip())
            heappush(min_heap, (val, chunk_index))

    # close all file handlers
    for fh in file_handlers:
        fh.close()

    # delete files
    for chunk in chunk_filenames:
        os.remove(chunk)
    
    return kth_largest

filename = "large_numbers.txt"

k = 10000
kth_largest = find_kth_largest(filename, k)
print(f"The {k}th largest element is: {kth_largest}")
