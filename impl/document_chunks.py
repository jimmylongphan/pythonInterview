from dataclasses import dataclass

@dataclass
class DocumentChunk:
    content: str
    offset: int

'''
Given a set of document chunks from a single source document, merge adjacent
chunks so that we return a list of document chunks with no overlap.

Example:
Given the following document:
document = 'Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say that they were perfectly normal, thank you very much.'

CHUNKS ARE NOT ORDERED 

# example 1
chunks1 = [
    DocumentChunk(content='Mr. and Mrs.', offset=0),
    DocumentChunk(content='Mrs. Dursley', offset=8),
    DocumentChunk(content=', Privet Drive', offset=36),
]
output1 = [
    DocumentChunk(content='Mr. and Mrs. Dursley', offset=0),
    DocumentChunk(content=', Privet Drive', offset=36),
]


# example 2
chunks2 = [
    DocumentChunk(content='number four', offset=25),
    DocumentChunk(content=', Privet Drive', offset=36),
]
output2 = [DocumentChunk(content='number four, Privet Drive', offset=25)]

overlap scenarios
    1. border -> overlap index is 0
    2. partial -> handled is > 0
    3. previous one is longer than current
'''

def merge_strings(retrieved_content: list[DocumentChunk]) -> list[DocumentChunk]:
    # sort the chunks by offset
    retrieved_content.sort(key=lambda x:x.offset)

    result = []
    chunk = retrieved_content[0]
    result.append(chunk)

    for chunk in retrieved_content[1:]:
        # previous chunk
        pre_chunk = result[-1]
        pre_end = len(pre_chunk.content) + pre_chunk.offset

        start_index = chunk.offset
        end_index = len(chunk.content) + chunk.offset

        # check overlap
        if start_index <= pre_end:
            # should end at with the longer chunk
            content = pre_chunk.content

            # merge slicing 
            if end_index >= pre_end:
                overlap_index = pre_end - start_index
                content += chunk.content[overlap_index:]

            pre_chunk.content = content 
            # offset is the same
        else:
            # add new chunk 
            result.append(chunk)

    return result

chunks1 = [
    DocumentChunk(content='Mr. and Mrs.', offset=0), #start 0, end is 12
    DocumentChunk(content='Mrs. Dursley', offset=8), #start is 8 -> offset + diff 
    DocumentChunk(content=', Privet Drive', offset=36),
]

output = merge_strings(chunks1)
print(output)

chunks2 = [
    DocumentChunk(content='number four', offset=25),
    DocumentChunk(content=', Privet Drive', offset=36),
]

output = merge_strings(chunks2)
print(output)


chunks3 = [
    DocumentChunk(content='number four, Privet Drive', offset=25),
    DocumentChunk(content='four', offset=32),
]

output = merge_strings(chunks3)
print(output)
