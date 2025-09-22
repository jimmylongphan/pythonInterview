import os
from collections import deque

class MerkleNode:
    def __init__(self, filename: str):
        self.filename = filename

        self.hash = ""

        # store the actual children
        self.children = []

        self.is_leaf = True


    def add_child(self, node):
        # add child
        self.is_leaf = False
        self.children.append(node)

        # compute hash
        self.hash_parent()


    def hash_leaf(self):
        # leaf node
        #   - no child directories

        # hash the contents
        with open(self.filename, 'rb') as file:
            data = file.read()
            hash_value = hash(data)
            self.hash = str(hash_value)

        print(f"  leaf node hash {self.hash}")


    def hash_parent(self):
        # parent node 
        #   - 
        #   - concatenat all children hashes, then hash again
        concatenated_hash = ""
        for child in self.children:
            concatenated_hash += str(child.hash)

        self.hash = hash(concatenated_hash)


# construct the tree
def construct_merkle_tree(dir: str) -> MerkleNode:
    # directory traversal of the file path
    root = None

    queue = deque()
    # queue is a tuple of (parent node, fileOrDirectory)
    queue.append((None, dir))

    # BFS 
    parent_nodes = []
    while queue:
        length = len(queue)

        for _ in range(length):
            parent, fileOrDir = queue.popleft()
            print(f"processing {fileOrDir}")
            node = MerkleNode(fileOrDir)

            # handle the current node
            if parent:
                parent.add_child(node)
                parent_nodes.append(parent)

            if os.path.isdir(fileOrDir):
                print(f"  is a dir")
                # get the children
                files = os.listdir(fileOrDir)
                print(f"    files {files}")
                for f in files:
                    child_fileOrDir = f"{fileOrDir}/{f}"
                    print(f"  appending {child_fileOrDir}")
                    queue.append((node, child_fileOrDir))

            elif os.path.isfile(fileOrDir):
                print(f"  is a file")
                node.hash_leaf()

            if not root:
                root = node

    # for all parents, compute their hashes
    for parent_node in parent_nodes:
        parent_node.hash_parent

    return root


if __name__ == "__main__":
    root = construct_merkle_tree("./postgres")
    print(f"root hash {root.hash}")

 