from typing import List, Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

#
# @lc app=leetcode id=94 lang=python3
#
# [94] Binary Tree Inorder Traversal
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        seq = []
        self.tr(root, seq)
        return seq

    def tr(self, root: Optional[TreeNode], seq: List[int]):
        if root is None:
            return
        self.tr(root.left, seq)
        seq.append(root.val)
        self.tr(root.right, seq)

# @lc code=end

