from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

#
# @lc app=leetcode id=110 lang=python3
#
# [110] Balanced Binary Tree
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def dump_tree(self, root: Optional[TreeNode]):
        if root is None:
            return 'null'
        return '{} l({}) r({})'.format(
            root.val,
            self.dump_tree(root.left),
            self.dump_tree(root.right)
        )

    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        h, b = self.heights(root)
        return b

    def heights(self, root: Optional[TreeNode]) -> List:
        if root is None:
            return 0, True
        lh, lb = self.heights(root.left)
        rh, rb = self.heights(root.right)
        return max(lh, rh) + 1, abs(lh - rh) < 2 and lb and rb

# @lc code=end

Solution().isBalanced(
    TreeNode(1,
             TreeNode(2,
                      TreeNode(4,
                               TreeNode(8)),
                      TreeNode(5)),
             TreeNode(3,
                      TreeNode(6))))

'''
1
    l(2
        l(4
            l(8)
            r(null)
        )
        r(5)
    )
    r(3
        l(6)
        r(null)
    )
'''