# Your previous Plain Text content is preserved below:

# # Introduction:

# Consider the data provided in the list below. You can assume that all the characters will always be lowercase and that each string contains no spaces.

# The comma-separated values can be interpreted in the following order:

# 1. A 64-bit integer representing the number of milliseconds since January 1, 1970 coordinated universal time (UTC). This is the time the sample was taken.
# 2. The partition number. There are 4 partitions, numbered 1 through 4.
# 3. The unique identifier for the asset that produced the sample represented as a Universally Unique Identifier (UUID).
# 4. The remainder of the line is a comma-separated list of hashtags. The valid hashtags are: #one, #two, #three, #four, #five, #six, #seven, #eight, #nine, #ten.

# ```
# data = [
#     "1505233687023,2,3c8f3f69-f084-4a0d-b0a7-ea183fabceef,#eight,#six,#five",
#     "1505233687036,2,ead3d58b-85f3-4f54-8e1e-b0a21ae99a0d,#five,#eight,#seven",
#     "1505233687037,2,345f7eb1-bf33-40c1-82a4-2f91c658803f,#two,#eight,#four,#nine,#ten,#three,#one,#seven,#six,#five",
#     "1505233687037,4,fe52fa24-4527-4dfd-be87-348812e0c736,#seven,#three,#six",
#     "1505233687037,4,120d688c-be5a-4e1f-a6ae-8614cb8e6af9,#ten,#seven,#eight,#one,#six,#five,#two,#four",
#     "1505233687037,1,ee838bbc-503a-4999-8654-bf51c173f82a,#three,#five,#six,#ten,#nine,#four,#one,#two",
#     "1505233687037,2,19624f23-9614-45b0-aa98-597112b891f9,#five,#three,#nine,#one,#ten,#six",
#     "1505233687038,4,c5966068-f777-4113-af4e-6eb2e14c3005,#one,#four,#three,#eight",
#     "1505233687038,4,9e1eb9c6-7691-4153-b431-74b157863b3e,#two,#five,#one,#seven,#nine,#six",
#     "1505233687038,1,67e4ce28-5495-481b-88b0-ca9247b80268,#seven,#five",
#     "1505233687038,3,3d71e733-be9a-4a0b-b435-4bbce1a8d090,#five,#seven,#two,#six,#one,#four,#ten",
#     "1505233687039,3,4fc18980-0f65-4033-b5b5-4a64effba2f5,#nine,#one,#ten,#two,#seven,#three,#eight,#six,#four",
#     "1505233687039,2,363a36ea-d984-4291-920c-550e40fb0821,#two,#eight,#five,#ten,#one,#seven",
#     "1505233687039,1,580dc11a-6818-45d5-8889-4ff9854f87d4,#three",
#     "1505233687039,3,2811b5f8-70d2-48ef-82d1-80b5ae8f7ec0,#five,#three,#one,#seven,#nine,#four,#eight,#two",
#     "1505233687040,4,cfbb2c7f-d8f4-4859-bf9f-d98d73a21d77,#nine,#eight,#one,#ten,#seven,#five,#six",
#     "1505233687043,2,4a740ab9-0893-4e4f-b769-2ea47643e13e,#eight,#three,#four,#five,#two",
#     "1505233687043,3,f4a037cb-ca36-4e31-9a74-1d2504fd35a4,#ten,#eight,#three,#six,#two,#one,#nine,#five,#seven,#four",
#     "1505233687044,3,c75ceb2c-1dfa-4584-8190-2dfd3da30b0f,#eight,#four,#nine,#two,#seven,#five,#six"
# ]
# ```

# # Requirements:
# ## Part 1:

# Write a program with the following requirements:

# 1. Interpret each line.
# 2. Map the hashtags associated with one sample to the equivalent integer between 1 and 10. For example, for the first line, the hashtags are #eight,#six,#five and should be mapped to the integers 8, 6, and 5, respectively.
# 3. Sum the set of integers mapped from the hashtags for each sample. For example, for the first line, the integers 8, 6, and 5 sum to 19.
# 4. Print each sample to the console, where the output is a comma-separated line with the timestamp, followed by the unique identifier, followed by the computed sum. For the first line above, the output should be: "1505233687023,3c8f3f69-f084-4a0d-b0a7-ea183fabceef,19"
# 5. Partition the samples based on the partition number when printing them. For each partition, the order of the samples in the output print statement should be the same as the order they appeared in the input file. The order of the partitions does not matter.

"""
Iterate through the lines 
    split by comma 
    process - partitions 
        element 3 to end - hash tags
        convert - map { "#one": 1 }
            running sum 
        create the output string
        append to the data structure 

data structure - map 
    key - partition 
    value - list 

output string format 
    f"{timestamp},{uuid},{sum}"

iterate through 1-4
    print out the list - ordered is maintained 
"""
from collections import defaultdict

hashtag_conversions = {
    "#one": 1,
    "#two": 2,
}

def converter(data: dict):
    output_partitions = defaultdict(list)

    for line in data:
        # min 4 elements
        tokens = line.split(",")

        # epoch time 
        # time library - read it
        timestamp = tokens[0]

        # convert to an int and check range 1-4
        partition = tokens[1]

        # uuid library, parse it 
        uuid = tokens[2]

        running_sum = 0
        for hashtag in tokens[3:]:
            running_sum += hashtag_conversions[hashtag]

        output_line = f"{timestamp},{uuid},{running_sum}"
        output_partitions[partition].append(output_line)



"""
high throughput
    - observabilitly of errors

Questions
- how to handle throughput
- how to handle tracing?

"""