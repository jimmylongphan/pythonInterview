class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.sibling = None  # Right sibling pointer

def print_level_by_level(root):
    if not root:
        return

    current = root
    while current:
        child = None

        # Traverse the current level using sibling pointers
        node = current
        while node:
            # get the next child 
            if not child and node.left:
                child = node.left
            if not child and node.right:
                child = node.right

            print(node.val, end=" ")
            node = node.sibling
        
        print()  # Move to the next line for the next level

        # set current to child for next printing 
        current = child

# Example usage
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
root.right.right = Node(6)

# Manually setting sibling pointers
root.left.sibling = root.right
root.left.left.sibling = root.left.right
root.left.right.sibling = root.right.right

print_level_by_level(root)
