from typing import Optional


class ListNode:
    def __init__(self, val=0, next = None):
        self.val = val
        self.next = next

#
# @lc app=leetcode id=2181 lang=python3
#
# [2181] Merge Nodes in Between Zeros
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        p = head
        pp = None
        while p.next is not None:
            while p.next.val > 0:
                p.val += p.next.val
                p.next = p.next.next
            pp = p
            p = p.next
        if pp is None:
            return None
        pp.next = None
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

def test(args): return from_list(Solution().mergeNodes(to_list(args)))
method = test

run_test(method, [[0,3,1,0,4,5,2,0]], [4, 11])
run_test(method, [[0,1,0,3,0,2,2,0]], [1, 3, 4])
run_test(method, [[0,1,0]], [1])
