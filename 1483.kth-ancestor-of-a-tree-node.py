#
# @lc app=leetcode id=1483 lang=python3
#
# [1483] Kth Ancestor of a Tree Node
#

# @lc code=start
from heapq import heappush
from typing import List, Optional
from functools import cache



class CacheItem:
    def __init__(self):
        self.d = {}
        self.ks = []

    def store(self, k: int, ancestor: int) -> None:
        self.d[k] = ancestor
        n = self._find_ki_after(k)
        if n is None:
            self.ks.append(k)
        else:
            self.ks.insert(n, k)

    def best_up_to(self, k: int):
        n = self._find_ki_after(k)
        if n is None or n == 0:
            return None
        n = self.ks[n - 1]
        return self.d[n], n

    def _find_ki_after(self, k: int):
        for i, n in enumerate(self.ks):
            if n > k:
                return i
        return None



class Cache:

    def __init__(self):
        self.data = {}

    def best_up_to(self, node: int, k: int) -> Optional[int]:
        if node not in self.data:
            return None
        return self.data[node].best_up_to(k)

    def store(self, node: int, k: int, ancestor: int) -> None:
        if node not in self.data:
            self.data[node] = CacheItem()
        self.data[node].store(k, ancestor)



class TreeAncestor:

    def __init__(self, n: int, parent: List[int]):
        self.parent = parent
        self.cache = Cache()

    def getKthAncestor(self, node: int, k: int) -> int:
        n = node
        i = k
        while True:
            r = self.cache.best_up_to(n, i)
            if r is None:
                break
            n, i = r

        while i > 0:
            n = self.parent[n]
            if n == -1:
                return -1
            i -= 1
        self.cache.store(node, k, n)
        return n



# Your TreeAncestor object will be instantiated and called as such:
# obj = TreeAncestor(n, parent)
# param_1 = obj.getKthAncestor(node,k)
# @lc code=end

ta = TreeAncestor(7, [-1, 0, 0, 1, 1, 2, 2])
print(ta.getKthAncestor(3, 1))
print(ta.getKthAncestor(5, 2))
print(ta.getKthAncestor(6, 3))

ta = TreeAncestor(7, [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21])

print(ta.getKthAncestor(3, 1))
print(ta.getKthAncestor(5, 2))
print(ta.getKthAncestor(6, 3))
print(ta.getKthAncestor(8, 2))
print(ta.getKthAncestor(10, 2))
print(ta.getKthAncestor(21, 19))