class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

#
# @lc app=leetcode id=23 lang=python3
#
# [23] Merge k Sorted Lists
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from typing import List, Optional
from heapq import heappop, heappush

setattr(ListNode, "__lt__", lambda self, other: self.val <= other.val)

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        h = []
        for l in lists:
            if l is not None:
                heappush(h, l)
        dumb_node = ListNode(0)
        p = dumb_node
        while len(h) > 0:
            n = heappop(h)
            if n.next is not None:
                heappush(h, n.next)
            p.next = n
            p = n
        return dumb_node.next
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

def test(lists):
    return from_list(Solution().mergeKLists(to_list(l) for l in lists))
method = test

run_test(method, [[[1,4,5],[1,3,4],[2,6]]], [1,1,2,3,4,4,5,6])
run_test(method, [[]], [])
run_test(method, [[[]]], [])