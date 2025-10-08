'''
Write and test a function called findTopK as follows:
 
- Input: a list of integers and an int k.
- Output: the k largest integers in the list.
- Assumptions:
   - Everything fits comfortably in memory.
   - The k largest items don't necessarily need to return in any particular sorted order.
   - If the list has duplicates, only return up to k items. 

- Examples:
   - findTopK([1,4,3,2], 3) produces [4,3,2] (or any ordering of this list).
   - findTopK([1,4,2,1], 3) produces [4,2,1] (or any ordering of this list).
'''
from heapq import heappush, heappop

def findTopK(nums, k) -> list:
    heap = []

    if k <= 0:
        raise Exception(f"invalid k value: {k}")

    for n in nums:
        if len(heap) < k:
            heappush(heap, n)
        elif heap[0] < n:
            # only pushes if new element is larger
            heappop(heap)
            heappush(heap, n)

    return heap

nums = [1,4,3,2]
k = 3
result = findTopK(nums, k)
print(f"result is {result}")

nums = [1,4,2,1]
result = findTopK(nums, k)
print(f"result is {result}")


nums = [1,-4,3,2]
result = findTopK(nums, k)
print(f"result is {result}")

result = findTopK(nums, -1)
print(f"result is {result}")