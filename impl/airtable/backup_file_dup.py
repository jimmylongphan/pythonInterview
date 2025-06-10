"""
Imagine that we are writing a backup application used to backup files from your laptop to a remote server. To save on network bandwidth, we want to identify duplicate files (i.e., files with the same contents). This way, we only need to upload duplicate files once.

Write a function that identifies sets of files with identical contents.

find_dupes(root_path) → sets/lists of 2 or more file paths that have identical contents

find_dupes("/home/airtable") → [
    [".bashrc", "Backups/2017_bashrc"],
    ["Photos/Vacation/DSC1234.JPG", "profile.jpeg", ".trash/lej2dp28/87msnlgyr"],
]

For scale, imagine running this on a computer with at most 2 TB of data and at most 1 million files.

For traversing the filesystem, use these library functions:

    list_folder(path) → list of names of immediate file and folder children
    is_folder(path) → boolean

hashlib.sha256()
hex_digest is 64 characters or 64 bytes
1 million files * 64 bytes
64 MB of memory for the hash table

Even larger
    - write to disk
"""
import hashlib
import os
from collections import defaultdict
from collections import deque

# read 1 MB chunks
CHUNK_SIZE = 1024 * 1024

def hash_file(path: str) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as file:
        while True:
            chunk = file.read(CHUNK_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

def find_dupes(root_path: str) -> list[str]:
    dup_map = defaultdict(list)

    queue = deque()
    queue.append(root_path)

    while queue:
        current = queue.pop()

        # for a folder, add the contents to the queue
        if os.path.isdir(current):
            contents = os.listdir(current)
            for item in contents:
                queue.append(current + "\\" + item)
        else:
            # for a file, get the hash and add to the map
            hash_value = hash_file(current)
            dup_map[hash_value].append(current)


    result = []
    for _, files in dup_map.items():
        if len(files) > 1:
            same_file_list = [fn for fn in files]
            result.append(same_file_list)

    return result

current_dir = "H:\\test_files"
result = find_dupes(current_dir)
print(f"result: {result}")
