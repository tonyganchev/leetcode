from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

#
# @lc app=leetcode id=92 lang=python3
#
# [92] Reverse Linked List II
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def reverseBetween(self, head: Optional[ListNode], left_idx: int, right_idx: int) -> Optional[ListNode]:
        if left_idx == right_idx:
            return head
        nh = ListNode(0, head)
        before_left = nh
        for i in range(left_idx - 1):
            before_left = before_left.next
        left = before_left.next
        right = left
        for i in range(left_idx, right_idx):
            right = right.next
        after_right = right.next
        print(left.val)
        print(right.val)
        print('--')
        
        p = left
        c = left.next
        while c != after_right:
            n = c.next
            c.next = p
            p = c
            c = n

        left.next = after_right
        before_left.next = right
        if before_left == nh:
            head = right

        pp = head
        while pp is not None:
            print(pp.val)
            pp = pp.next

        return head
        
# @lc code=end

Solution().reverseBetween(
    ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5))))),
    2, 4
)
print('-----------------')
Solution().reverseBetween(
    ListNode(3, ListNode(5)),
    1, 2
)
