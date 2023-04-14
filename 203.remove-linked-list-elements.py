from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

#
# @lc app=leetcode id=203 lang=python3
#
# [203] Remove Linked List Elements
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        nh = ListNode(0, head)
        p = nh
        while p is not None:
            q = p.next
            while q is not None:
                if q.val == val:
                    q = q.next
                else:
                    break
            p.next = q
            p = p.next
        return nh.next
# @lc code=end

