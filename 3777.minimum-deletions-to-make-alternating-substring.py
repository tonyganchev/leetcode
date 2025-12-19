#
# @lc app=leetcode id=3777 lang=python3
#
# [3777] Minimum Deletions to Make Alternating Substring
#

from typing import List

# @lc code=start

class FenwickTree:
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)

    def get_sum(self, i: int) -> int:
        s = 0
        i += 1
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def update(self, i: int, v):
        i += 1
        while i <= self.n:
            self.tree[i] += v
            i += i & (-i)


class String:
    def __init__(self, s: str):
        self.s = list(s)
        self.ft = FenwickTree(len(s))
        
        for i in range(1, len(s)):
            self.ft.update(i, 1 if s[i] == s[i - 1] else 0)

    def flip(self, i: int):
        self.s[i] = 'A' if self.s[i] == 'B' else 'B'
        if i > 0:
            self.ft.update(i, 1 if self.s[i] == self.s[i - 1] else -1)
        if i < len(self.s) - 1:
            self.ft.update(i + 1, 1 if self.s[i + 1] == self.s[i] else -1)

    def min_del(self, l: int, r: int) -> int:
        return self.ft.get_sum(r) - self.ft.get_sum(l)


class Solution:
    def minDeletions(self, s: str, queries: List[List[int]]) -> List[int]:
        s = String(s)
        
        qr = []
        for q in queries:
            if q[0] == 1:
                s.flip(q[1])
            else:
                qr.append(s.min_del(q[1], q[2]))
        return qr

# @lc code=end

from test_utils import run_test

def test(s, q):
    return Solution().minDeletions(s, q)
method = test

run_test(method, ["BBABBB", [[1,5],[2,2,5]]], [1])
run_test(method, ["ABA", [[2,1,2],[1,1],[2,0,2]]], [0,2])
run_test(method, ["ABB", [[2,0,2],[1,2],[2,0,2]]], [1,0])
run_test(method, ["BABA", [[2,0,3],[1,1],[2,1,3]]], [0,1])
run_test(method, ["BA", [[1,0],[2,0,1]]], [1])
