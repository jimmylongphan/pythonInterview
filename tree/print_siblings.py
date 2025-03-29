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
        # Traverse the current level using sibling pointers
        node = current
        while node:
            print(node.val, end=" ")
            node = node.sibling
        print()  # Move to the next line for the next level

        # Move to the next level (find the leftmost node of the next level)
        if current.left:
            current = current.left
        elif current.right:
            current = current.right
        else:
            # Find the first child in the next level using sibling pointers
            temp = current.sibling
            while temp:
                if temp.left:
                    current = temp.left
                    break
                if temp.right:
                    current = temp.right
                    break
                temp = temp.sibling
            else:
                break  # If no children found, we're done

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
