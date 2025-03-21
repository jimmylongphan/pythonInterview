def bucket_sort(arr: list[int]) -> list[int]:
    # get max value to set num of buckets
    max_value = max(arr)

    # initialize and create buckets
    num_buckets = len(arr)
    buckets = [[] for _ in range(num_buckets)]

    # distribute elements 
    for n in arr:
        # special scaling bucketizing
        # multiply the current number by buckets to get a larger scaled number
        # divide by the max value + 1 to distribute into buckets
        # The numbers are distributed such that each bucket is larger than previous bucket
        # then sort the individual buckets
        # Bucket 4: [32, 33, 37]
        # Bucket 5: [42]
        # Bucket 6: [52, 47, 51]
        index = int(n * num_buckets / (max_value + 1))
        
        # add this value to the bucket
        buckets[index].append(n)

    # have to sort each buckety
    for b in buckets:
        b.sort()

    # concatenate the sorted buckets
    # this works because each bucket has a distributed of numbers that fit
    # then sort them
    # so we can concatenate them one by one
    result = []
    for b in buckets:
        result.extend(b)

    return result 

"""
Bucket 0: []
Bucket 1: []
Bucket 2: []
Bucket 3: []
Bucket 4: [32, 33, 37]
Bucket 5: [42]
Bucket 6: [52, 47, 51]
"""
arr = [42, 51, 32, 33, 52, 37, 47, 51]
sorted_arr = bucket_sort(arr)
print("Sorted Array:", sorted_arr)
