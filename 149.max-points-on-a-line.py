#
# @lc app=leetcode id=149 lang=python3
#
# [149] Max Points on a Line
#

# @lc code=start
from typing import List


class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        pc_max = 2
        for i in range(len(points) - 1):
            for j in range(i + 1, len(points)):
                x1, y1 = points[i]
                x2, y2 = points[j]
                
                if x1 == x2:
                    pc = 0
                    for xk, _ in range(len(points)):
                        if xk == x1:
                            pc += 1
                    pc_max = max(pc, pc_max)
                    continue

                


# @lc code=end

