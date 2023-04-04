class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


#
# @lc app=leetcode id=83 lang=python3
#
# [83] Remove Duplicates from Sorted List
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from typing import Optional


class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        p = head
        while p is not None:
            q = p.next
            while q is not None:
                if p.val == q.val:
                    q = q.next
                else:
                    break
            p.next = q
            p = p.next
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

def test(arg):
    in_list = to_list(arg)
    Solution().deleteDuplicates(in_list)
    return from_list(in_list)
method = test

from test_utils import run_test

run_test(method, [(1,)], [1,])
run_test(method, [(1,1)], [1,])
run_test(method, [(1,2)], [1,2])
run_test(method, [(1,1,2)], [1,2])
run_test(method, [(1,2,2)], [1,2])
run_test(method, [(1,1,2,2,)], [1,2])



