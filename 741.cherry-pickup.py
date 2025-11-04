#
# @lc app=leetcode id=741 lang=python3
#
# [741] Cherry Pickup
#

# @lc code=start
from typing import List


class Solution:
    def cherryPickup(self, grid: List[List[int]]) -> int:
        cache = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]
        return self.test(grid, 0, 0, cache)

    def test(self, grid: List[List[int]], row: int, col: int, cache: List[List[int]]) -> int:
        assert row < len(grid)
        assert col < len(grid[0])
        assert grid[row][col] != -1
        r = cache[row][col]
        if r == -1:
            d = grid[row][col]
            r = d
            if row == len(grid) - 1 and col == len(grid[0]) - 1:
                pass
            else:
                if row < len(grid) - 1 and grid[row + 1][col] != -1:
                    r = max(r, d + self.test(grid, row + 1, col, cache))
                if col < len(grid[0]) - 1 and grid[row][col + 1] != -1:
                    r = max(r, d + self.test(grid, row, col + 1, cache))
            cache[row][col] = r
        return r

# @lc code=end

from test_utils import run_test

method = Solution().cherryPickup

run_test(method, [[[0,1,-1],[1,0,-1],[1,1,1]]], 5)
run_test(method, [[[1,1,-1],[1,-1,1],[-1,1,1]]], 0)
