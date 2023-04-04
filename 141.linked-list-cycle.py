from typing import Optional

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


#
# @lc app=leetcode id=141 lang=python3
#
# [141] Linked List Cycle
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None



class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        p = head
        if p is None:
            return False
        q = p.next
        while True:
            if q is None:
                return False
            if p == q:
                return True
            p = p.next
            q = q.next
            if q is None:
                return False
            q = q.next
# @lc code=end

