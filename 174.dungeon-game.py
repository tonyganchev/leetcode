#
# @lc app=leetcode id=174 lang=python3
#
# [174] Dungeon Game
#

# @lc code=start
from typing import List

infinity = 1000000

class Solution:
    def calculateMinimumHP(self, dungeon: List[List[int]]) -> int:
        health_cache = [[-1 for _ in range(len(dungeon[0]))] for _ in range(len(dungeon))]
        h = self.test(dungeon, 0, 0, health_cache)
        return h

    def test(self, dungeon: List[List[int]], row: int, col: int, cache: List[List[int]]) -> int:
        h = cache[row][col]
        if h == -1:
            if row == len(dungeon) - 1 and col == len(dungeon[0]) - 1:
                h = max(1, -dungeon[row][col] + 1)
            else:
                if row == len(dungeon) - 1:
                    hd = infinity
                else:
                    hd = self.test(dungeon, row + 1, col, cache)
                if col == len(dungeon[0]) - 1:
                    hr = infinity
                else:
                    hr = self.test(dungeon, row, col + 1, cache)
                h2 = min(hd, hr)
                h = max(1, -dungeon[row][col] + h2)
            cache[row][col] = h
        return h


# @lc code=end

from test_utils import run_test

method = Solution().calculateMinimumHP

run_test(method, [[[-2,-3,3],[-5,-10,1],[10,30,-5]]], 7)
run_test(method, [[[0]]], 1)
