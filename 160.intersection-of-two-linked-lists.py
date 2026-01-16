#
# @lc app=leetcode id=160 lang=python3
#
# [160] Intersection of Two Linked Lists
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        visited_nodes = set()
        p = headA
        while p is not None:
            visited_nodes.add(id(p))
            p = p.next
        p = headB
        while p is not None:
            if id(p) in visited_nodes:
                return p
            p = p.next
# @lc code=end

