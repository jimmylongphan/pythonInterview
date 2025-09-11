class Node:
    def __init__(self, key: int, val: int):
        self.key = key
        self.val = val
        self.pre = self
        self.next = self

class LRUCache:
    def __init__(self, capacity: int):
        self.map = {}
        self.capacity = capacity
        self.sentinel_head = Node(0, 0)
        self.sentinel_tail = Node(0, 0)

        self.sentinel_head.next = self.sentinel_tail
        self.sentinel_tail.pre = self.sentinel_head
        
    def get(self, key: int) -> int:
        if key not in self.map:
            return -1

        node = self.map[key]

        # remove node
        # insert back at end
        self.remove_node(node)
        self.insert_node(node)

        return node.val

    def put(self, key: int, value: int) -> None:
        # check if exists
        if key not in self.map:
            # create the node
            node = Node(key, value)
            self.map[key] = node
        else:
            node = self.map[key]
            node.val = value
            # remove for later inset
            self.remove_node(node)

        self.insert_node(node)

        # handle capacity
        current_cap = len(self.map.keys())
        if current_cap > self.capacity:
            head = self.sentinel_head.next
            del self.map[head.key]
            self.remove_node(head)

    def delete(self, key: int):
        if key not in self.map:
            return
        
        # remove this specific node
        node = self.map[key]
        del self.map[key]
        self.remove_node(node)


    def last(self) -> int:
        """
        Get the most recently accessed value
        """
        tail = self.sentinel_tail.pre
        return tail.val

    def remove_node(self, node: Node):
        # update pointers
        pre = node.pre
        nxt = node.next

        pre.next = nxt
        nxt.pre = pre

    def insert_node(self, node: Node):
        # insert at the end
        pre = self.sentinel_tail.pre
        nxt = self.sentinel_tail

        pre.next = node
        node.pre = pre

        node.next = nxt
        nxt.pre = node


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)

cache = LRUCache(4)
cache.put(1, 1)
print(f"last is {cache.last()}")

cache.put(2, 2)
cache.put(3, 3)
print(f"last is {cache.last()}")

cache.get(2)
print(f"last is {cache.last()}")

cache.delete(2)
print(f"deleting 2, last is {cache.last()}")

