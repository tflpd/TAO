from src.flags import VERBOSE_FLAG


# QNode -> holds key and value; as well as pointers to previous and next nodes.
from src.structs import Object, assocs_to_str


class QNode(object):
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


class LList(object):
    def __init__(self, capacity):
        self.head = None
        self.end = None
        self.capacity = capacity
        self.current_size = 0


class LRUCache(object):
    def __init__(self, capacity):

        #:type capacity: int

        if capacity <= 0:
            raise ValueError("capacity > 0")
        self.hash_map = {}

        self.LList = LList(capacity)

    # PUBLIC

    def get_element(self, key):

        #:rtype: int

        if key not in self.hash_map:
            return -1

        node = self.hash_map[key]

        # small optimization (1): just return the value if we are already looking at head
        if self.LList.head == node:
            return node.value
        self.remove(node)
        self.set_head(node)
        return node.value

    def set(self, key, value):

        #:type key: int
        #:type value: int
        #:rtype: nothing

        if key in self.hash_map:
            node = self.hash_map[key]
            node.value = value

            # small optimization (2): update pointers only if this is not head; otherwise return
            if self.LList.head != node:
                self.remove(node)
                self.set_head(node)
        else:
            new_node = QNode(key, value)
            if self.LList.current_size == self.LList.capacity:
                del self.hash_map[self.LList.end.key]
                self.remove(self.LList.end)
            self.set_head(new_node)
            self.hash_map[key] = new_node

    # PRIVATE

    def set_head(self, node):
        if not self.LList.head:
            self.LList.head = node
            self.LList.end = node
        else:
            node.prev = self.LList.head
            self.LList.head.next = node
            self.LList.head = node
        self.LList.current_size += 1

    def remove(self, node):
        if not self.LList.head:
            return

        # removing the node from somewhere in the middle; update pointers
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev

        # head = end = node
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
            print("%s ->\n" % (n.value), end="")
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
            print("%s ->\n" % (string3), end="")
            tmp_node = tmp_node.prev
        print("NULL")

