"""
PROMPT

Write a command line interface

input
  - word: to be seearched in all documents

output
    <FileName>: <total occurrences> [1,2,6,…]
        1,2,6 are the line numbers where the word appears
        counts = all occurences of word in that file
        line numbers appear only once in the list
    lines are sorted by highest occurrences first

assumption:
  - all files are in the data directory
  - flat directory
  - if there is a nested directories, will use BFS to process it
"""
import re
import os

class FileData:
    def __init__(self, filename, word):
        self.filename = filename
        self.word = word
        self.word_count = 0
        self.lines = []

    def count_word(self, word: str, line: str, line_num: int):
        # split does not handle punctuation too well
        # convert to lower case, and trim white spaces for processing
        word_list = re.findall(r"\w+", line.lower().strip())
        count = word_list.count(word)
        if count > 0:
            self.word_count += count
            self.lines.append(line_num)

    def __lt__(self, other):
        """
        sort by word count greater first
        """
        return self.word_count > other.word_count

    def __str__(self):
        """
        <FileName>: <total occurrences> [1,2,6,...]
        1,2,6 are line numbers where word occurred
        """
        return f"{self.filename}: {self.word_count} {self.lines}"

def process_file(word: str, filename: str) -> FileData:
    with open(filename, "r") as file:
        filedata = FileData(filename, word)
        for line_number, line in enumerate(file, start=1):
            if line:
                filedata.count_word(word=word, line=line, line_num=line_number)
        if filedata.word_count > 0:
            return filedata

    return None


# @param word - the word to search in all documents
# @return - list of filedata
def search_word(dir: str, word: str) -> list[FileData]:
    """
    """
    # print(f"searching for {word} in {dir}")
    file_list = os.listdir(dir)
    filedata_list = []
    for filename in file_list:
        filename = os.path.join(dir, filename)
        if os.path.isfile(filename):
            # filename = f"{dir}/{filename}"
            # print(f"processing file {filename}")
            filedata = process_file(word=word, filename=filename)
            if filedata:
                filedata_list.append(filedata)
        elif os.path.isdir(filename):
            raise TypeError(f"{filename} is a directory")

    # sort the filedata
    # most occurrences should appear first
    filedata_list.sort()
    return filedata_list


if __name__ == "__main__":
    print("Please enter a word to search --> ", end="")
    word = input()
    # make lower case to make case insensitive
    word = word.lower()

    dir = "./data"
    filedata_list = search_word(dir=dir, word=word)
    for fd in filedata_list:
        print(fd)
