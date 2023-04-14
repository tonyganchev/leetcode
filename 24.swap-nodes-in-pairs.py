from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

#
# @lc app=leetcode id=24 lang=python3
#
# [24] Swap Nodes in Pairs
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        bl = None
        l = head
        if l is None:
            return head
        r = head.next
        if r is None:
            return head
        ar = r.next
        while True:
            if bl is not None:
                bl.next = r
            l.next = ar
            r.next = l
            if l == head:
                head = r
            bl = l
            l = ar
            if l is None:
                break
            r = l.next
            if r is None:
                break
            ar = r.next
        return head

# @lc code=end

def to_list(arr):
    head = None
    p = None
    for a in arr:
        if head is None:
            head = ListNode(a)
            p = head
        else:
            p.next = ListNode(a)
            p = p.next
    return head

def from_list(head):
    r = []
    while head is not None:
        r.append(head.val)
        head = head.next
    return r

from test_utils import run_test

def test(args): return from_list(Solution().swapPairs(to_list(args)))
method = test

run_test(method, [[]], [])
run_test(method, [[1]], [1])
run_test(method, [[1, 2]], [2, 1])
run_test(method, [[1, 2, 3]], [2, 1, 3])
run_test(method, [[1, 2, 3, 4]], [2, 1, 4, 3])
run_test(method, [[1, 2, 3, 4, 5]], [2, 1, 4, 3, 5])
run_test(method, [[1, 2, 3, 4, 5, 6]], [2, 1, 4, 3, 6, 5])
run_test(method, [[1, 2, 3, 4, 5, 6, 7]], [2, 1, 4, 3, 6, 5, 7])
