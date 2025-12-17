#
# @lc app=leetcode id=304 lang=python3
#
# [304] Range Sum Query 2D - Immutable
#

from typing import List
# @lc code=start
from functools import cache

class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        self.matrix = matrix

        @cache
        def sumRegion(row1: int, col1: int, row2: int, col2: int) -> int:
            if row1 > row2 or col1 > col2:
                return 0
            if row1 == row2 and col1 == col2:
                return self.matrix[row1][col1]
            return sumRegion(row1, col1, row1, col1) + \
                sumRegion(row1, col1 + 1, row1, col2) + \
                sumRegion(row1 + 1, col1, row2, col2)
        
        self._sumRegion = sumRegion
        
    def sumRegion(self, row1, col1, row2, col2):
        return self._sumRegion(row1, col1, row2, col2)

# Your NumMatrix object will be instantiated and called as such:
# obj = NumMatrix(matrix)
# param_1 = obj.sumRegion(row1,col1,row2,col2)
# @lc code=end

from test_utils import run_test

a = NumMatrix([[3,0,1,4,2],[5,6,3,2,1],[1,2,0,1,5],[4,1,0,1,7],[1,0,3,0,5]])
def test(m, v):
    return m.sumRegion(*v)
method = test

run_test(method, [a, [2,1,4,3]], 7)
run_test(method, [a, [1,1,2,2]], 7)
run_test(method, [a, [1,2,2,4]], 7)
