#
# @lc app=leetcode id=1515 lang=python3
#
# [1515] Best Position for a Service Centre
#

# @lc code=start
from math import sqrt
from typing import List
import numpy as np
from scipy.spatial import ConvexHull

class Solution:
    def getMinDistSum(self, positions: List[List[int]]) -> float:

        if len(positions) == 1:
            return 0.0

        if len(positions) == 2:
            (x1, y1), (x2, y2) = positions
            return 2 * sqrt((x2 - x1) ** 2 / 4 + (y2 - y1) ** 2 / 4)

        hull = ConvexHull(positions)

        #Get centoid
        cx = np.mean(hull.points[hull.vertices,0])
        cy = np.mean(hull.points[hull.vertices,1])

        d = 0.0

        for x, y in positions:
            d += sqrt((cx - x) ** 2 + (cy - y) ** 2)

        return d

# @lc code=end

from test_utils import run_test

method = Solution().getMinDistSum

run_test(method, [[[0,1],[1,0],[1,2],[2,1]]], 4.0)
run_test(method, [[[1,1],[3,3]]], 2.82843)
run_test(method, [[[1,1]]], 0.0)
run_test(method, [[[1,1],[0,0],[2,0]]], 2.73205)