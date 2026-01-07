class ListNode:
    
    def __init__(self, key):
        self.count = 1
        self.keys = set((key,))
        self.prev = None
        self.next = None

    def __str__(self):
        left = "x-" if self.prev is None else f'{self.prev.count}<-'
        right = "-x" if self.next is None else f'->{self.next.count}'
        return left + f'{self.count}|{self.keys}' + right

class MinMaxList:
    
    def __init__(self):
        self.head = None
    
    def add(self, key):
        if self.head is None:
            new = ListNode(key)
            new.prev = new
            new.next = new
            self.head = new
            return self.head.prev

        old_last = self.head.prev
        
        if old_last.count == 1:
            old_last.keys.add(key)
            return old_last

        new = ListNode(key)
        old_last.next = new
        new.prev = old_last
        self.head.prev = new
        new.next = self.head
        return self.head.prev

    def increase(self, node, key):
        larger_node = node.prev
        smaller_node = node.next
        if len(node.keys) == 1:
            if larger_node.count == node.count + 1:
                # move key to the prvious node and dispose of this node
                larger_node.keys.add(key)
                larger_node.next = smaller_node
                smaller_node.prev = larger_node
                return larger_node
            else:
                # We can simply increase the count on the node and keep the
                # node
                node.count += 1
                return node

        if larger_node == node:
            # only one node in the list
            assert smaller_node == node
            # A new node is put in front of the current node
            node.keys.remove(key)
            new = ListNode(key)
            new.count = node.count + 1
            new.next = node
            node.prev = new
            new.prev = node
            node.next = new
            self.head = new
            return new

        if larger_node.count == node.count + 1:
            larger_node.keys.add(key)
            node.keys.remove(key)
            return larger_node

        # A new node is put in front of the current node
        node.keys.remove(key)
        new = ListNode(key)
        new.count = node.count + 1
        new.next = node
        node.prev = new
        new.prev = larger_node
        larger_node.next = new
        if self.head == node:
            self.head = new
        return new

    def decrease(self, node, key):
        larger_node = node.prev
        smaller_node = node.next

        if node.count == 1:
            if len(node.keys) == 1:
                if larger_node == node:
                    self.head = None
                else:
                    larger_node.next = smaller_node
                    smaller_node.prev = larger_node
                    assert self.head != node
            else:
                node.keys.remove(key)
            return None

        if len(node.keys) == 1:
            if smaller_node.count == node.count - 1:
                smaller_node.keys.add(key)
                larger_node.next = smaller_node
                smaller_node.prev = larger_node
                if self.head == node:
                    self.head = smaller_node
                return smaller_node
            node.count -= 1
            return node
        
        if smaller_node == node:
            # single node
            node.keys.remove(key)
            new = ListNode(key)
            node.next = new
            new.prev = node
            node.prev = new
            new.next = node
            return new

        if smaller_node.count == node.count - 1:
            smaller_node.keys.add(key)
            node.keys.remove(key)
            return smaller_node
        
        node.keys.remove(key)
        new = ListNode(key)
        new.count = node.count - 1
        new.next = smaller_node
        new.prev = node
        node.next = new
        smaller_node.prev = node
        return new

    def min(self):
        if self.head is None:
            return ''
        for key in self.head.prev.keys:
            return key
        return ''

    def max(self):
        if self.head is None:
            return ''
        for key in self.head.keys:
            return key
        return ''

    def validate_invariants(self):
        if self.head is None:
            return
        p = self.head
        c = p.next
        
        while c != self.head:
            assert p == c.prev
            p = c
            c = c.next


class AllOne:

    def __init__(self):
        self.list = MinMaxList()
        self.map = {}

    def inc(self, key: str) -> None:
        node = self.list.increase(self.map[key], key) if key in self.map \
            else self.list.add(key)
        self.map[key] = node
        self._validate_invariants()

    def dec(self, key: str) -> None:
        new_node = self.list.decrease(self.map[key], key)
        if new_node is None:
            del self.map[key]
        else:
            self.map[key] = new_node
        self._validate_invariants()

    def getMaxKey(self) -> str:
        return self.list.max()

    def getMinKey(self) -> str:
        return self.list.min()

    def _validate_invariants(self):
        self.list.validate_invariants()
        for k, v in self.map.items():
            assert k in v.keys
            assert v.prev.next == v
            assert v.next.prev == v

# Your AllOne object will be instantiated and called as such:
# obj = AllOne()
# obj.inc(key)
# obj.dec(key)
# param_3 = obj.getMaxKey()
# param_4 = obj.getMinKey()

c = AllOne()

c.inc('a')
c.inc('b')
c.inc('c')
c.inc('d')
c.inc('e')
c.inc('f')
c.inc('g')
c.inc('h')
c.inc('i')
c.inc('j')
c.inc('k')
c.inc('l')

c.dec('a')
c.dec('b')
c.dec('c')
c.dec('d')
c.dec('e')
c.dec('f')

c.inc('g')
c.inc('h')
c.inc('i')
c.inc('j')

assert c.getMaxKey() in {'g', 'h', 'i', 'j'}
assert c.getMinKey() in {'k', 'l'}


c = AllOne()
c.inc('hello')
c.inc('goodbye')
c.inc('hello')
c.inc('hello')
assert c.getMaxKey() == 'hello'
assert c.getMinKey() == 'goodbye'
c.inc('leet')
assert c.getMaxKey() == 'hello'
c.inc('code')
assert c.getMaxKey() == 'hello'
c.inc('leet')
assert c.getMaxKey() == 'hello'
c.dec('hello')
assert c.getMaxKey() in {'hello', 'leet'}
c.inc('leet')
assert c.getMaxKey() == 'leet'
c.inc('code')
c.inc('code')
assert c.getMaxKey() == 'leet'