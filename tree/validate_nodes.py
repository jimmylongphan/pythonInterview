class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def find_binary_tree_root(nodes):
    if not nodes:
        return None

    parent_map = {}  # Maps each node to its parent
    all_nodes = set(nodes)  # Store all nodes for easy lookup

    # Build parent mapping
    for node in nodes:
        for child in (node.left, node.right):
            if child:
                if child in parent_map:  # Child already has a parent (invalid case)
                    return None
                parent_map[child] = node

    # Find the root (node without a parent)
    root = None
    for node in nodes:
        if node not in parent_map:  # This should be the only root
            if root:  # More than one root found (invalid case)
                return None
            root = node

    if not root:  # No root found
        return None

    # Validate tree structure
    if not is_valid_tree(root, nodes):
        return None

    return root

def is_valid_tree(root, nodes):
    """ Checks if the tree has cycles and all nodes are reachable. """
    visited = set()
    stack = [root]

    while stack:
        node = stack.pop()
        if node in visited:
            return False  # Cycle detected
        visited.add(node)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    return len(visited) == len(nodes)  # Ensure all nodes are reachable
