from src.flags import VERBOSE_FLAG
from src.structs import assocs_to_str


class LRUCacheNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

    def __str__(self):
        if VERBOSE_FLAG:
            return "(%s, %s)" % (self.key, self.value)
        else:
            return str(self.key)


# Note; this is an inversed LinkedList so you may think of the head being the rightmost
# element instead of the usual leftmost
class LList:
    def __init__(self, capacity):
        self.head = None
        self.end = None
        self.capacity = capacity
        self.current_size = 0


# A least recently used policy cache. In this implementation it is used for caching both objects and
# associations lists by using the respective keys
class LRUCache:
    def __init__(self, capacity):

        if capacity <= 0:
            raise ValueError("capacity > 0")
        self.hash_map = {}

        self.LList = LList(capacity)

    def set_first(self, node):
        if not self.LList.head:
            self.LList.head = node
            self.LList.end = node
        else:
            node.prev = self.LList.head
            self.LList.head.next = node
            self.LList.head = node
        self.LList.current_size += 1

    def delete(self, node):
        if not self.LList.head:
            return

        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev

        # if this was the only node
        if not node.next and not node.prev:
            self.LList.head = None
            self.LList.end = None

        # if the node we are removing is the one at the end, update the new end
        # also not completely necessary but set the new end's previous to be NULL
        if self.LList.end == node:
            self.LList.end = node.next
            self.LList.end.prev = None
        self.LList.current_size -= 1
        return node

    def print_objects(self):
        print("{LOG} Printing LRU's objects...")
        n = self.LList.head
        print("[head = " + str(self.LList.head) + ", end = " + str(self.LList.end) + "]  LIST:\n", end=" ")
        while n:
            print("%s ->\n" % n.value, end="")
            n = n.prev
        print("NULL")

    def print_assocs(self):
        print("{LOG} Printing LRU's associations...")
        tmp_node = self.LList.head
        string1 = assocs_to_str(assocs=self.LList.head.value)
        string2 = assocs_to_str(assocs=self.LList.end.value)
        print("[head = " + string1 + ", end = " + string2 + "]  LIST:\n", end="")
        while tmp_node:
            string3 = assocs_to_str(tmp_node.value)
            print("%s ->\n" % string3, end="")
            tmp_node = tmp_node.prev
        print("NULL")

    def get_element(self, key):

        if key not in self.hash_map:
            return -1

        node = self.hash_map[key]

        # if this key was already the last accessed no other changes are needed
        if self.LList.head == node:
            return node.value
        self.delete(node)
        self.set_first(node)
        return node.value

    def set(self, key, value):

        if key in self.hash_map:
            node = self.hash_map[key]
            node.value = value

            # if this key was already the last accessed no other changes are needed
            if self.LList.head != node:
                self.delete(node)
                self.set_first(node)
        else:
            new_node = LRUCacheNode(key, value)
            if self.LList.current_size == self.LList.capacity:
                del self.hash_map[self.LList.end.key]
                self.delete(self.LList.end)
            self.set_first(new_node)
            self.hash_map[key] = new_node

