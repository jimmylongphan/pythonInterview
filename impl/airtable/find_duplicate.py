class Solution:
    def findDuplicate(self, paths: List[str]) -> List[List[str]]:
        result = []

        dup_map = defaultdict(list)

        # iterate through the paths
        for path in paths:
            # parse the path line
            tokens = path.split(" ")
            root = tokens[0]

            # iterate through the files and contents
            for item in tokens[1:]:
                parenthesis_index = item.index("(")
                file_name = item[:parenthesis_index]
                file_content = item[parenthesis_index+1:-1]
                file_name = root + "/" + file_name
                dup_map[file_content].append(file_name)

        for _, file_names in dup_map.items():
            if len(file_names) > 1:
                same_file_list = [fn for fn in file_names]
                result.append(same_file_list)

        return result
