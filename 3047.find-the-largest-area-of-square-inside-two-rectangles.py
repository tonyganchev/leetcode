#
# @lc app=leetcode id=3047 lang=python3
#
# [3047] Find the Largest Area of Square Inside Two Rectangles
#

from typing import List

# @lc code=start

from itertools import chain

class Solution:
    def largestSquareArea(self, bottomLeft: List[List[int]], topRight: List[List[int]]) -> int:
        best = 0
        for i in range(len(bottomLeft) - 1):
            for j in range(i + 1, len(bottomLeft)):
                w = min(topRight[i][0], topRight[j][0]) - max(bottomLeft[i][0], bottomLeft[j][0])
                h = min(topRight[i][1], topRight[j][1]) - max(bottomLeft[i][1], bottomLeft[j][1])
                if w > 0 and h > 0:
                    best = max(best, min(w, h) ** 2)
        return best

# @lc code=end

from test_utils import run_test

def test(bottomLeft, topRight):
    return Solution().largestSquareArea(bottomLeft, topRight)

run_test(test, [[[2,2],[3,1]], [[5,5],[5,5]]], 4)
run_test(test, [[[1,1],[1,3],[1,5]], [[5,5],[5,7],[5,9]]], 4)
run_test(test, [[[1,1],[2,2],[3,1]], [[3,3],[4,4],[6,6]]], 1)
run_test(test, [[[1,1],[2,2],[1,2]], [[3,3],[4,4],[3,4]]], 1)
run_test(test, [[[1,1],[3,3],[3,1]], [[2,2],[4,4],[4,2]]], 0)
