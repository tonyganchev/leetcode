#
# @lc app=leetcode id=2267 lang=python3
#
# [2267]  Check if There Is a Valid Parentheses String Path
#

# @lc code=start
from typing import List


class Solution:
    def __init__(self) -> None:
        self.cache = {}
        
    def hasValidPath(self, grid: List[List[str]]) -> bool:
        return self.test(grid, 0, 0, 0)

    def test(self, grid: List[List[str]], row: int, col: int, stack: int) -> bool:
        if row == len(grid) or col == len(grid[0]):
            return False
        if grid[row][col] == '(':
            stack += 1
            if stack > (len(grid) - row + len(grid[0]) - col - 2):
                return False
        else:
            stack -= 1
            if stack < 0:
                return False
        if row == len(grid) - 1 and col == len(grid[0]) - 1:
            return stack == 0
        
        coords = row, col, stack
        if coords in self.cache:
            return self.cache[coords]

        r = self.test(grid, row + 1, col, stack) \
            or self.test(grid, row, col + 1, stack)
        self.cache[coords] = r

        return r

# @lc code=end

from test_utils import run_test

def test(grid): return Solution().hasValidPath(grid)
method = test

run_test(method, [[["(","(","("],[")","(",")"],["(","(",")"],["(","(",")"]]], True)
run_test(method, [[[")",")"],["(","("]]], False)
run_test(method, [[["(",")",")","(","(","(","(",")",")","(",")","(",")","(","(","(","(",")","(",")","("],["(","(",")",")","(",")",")",")","(",")","(",")","(","(",")","(","(","(","(","(",")"],[")",")","(",")",")","(","(",")","(","(",")","(",")",")","(",")",")","(","(",")",")"],["(","(",")","(",")","(",")",")",")","(",")","(","(",")","(",")",")","(",")",")",")"],["(","(","(",")","(","(",")","(",")",")","(",")",")",")",")",")",")","(",")","(","("],[")",")","(","(",")",")",")",")",")","(",")",")",")","(","(",")","(","(","(","(",")"],[")",")",")",")","(",")","(",")","(","(",")","(","(",")","(","(",")",")","(",")","("],["(",")","(","(","(",")",")",")",")","(","(",")","(","(",")",")","(",")",")",")","("],["(",")","(",")","(","(","(","(",")","(","(","(","(","(","(",")","(",")","(",")",")"],["(",")","(","(","(",")","(",")",")",")",")","(","(","(","(",")",")","(","(","(",")"],["(","(",")","(",")",")","(",")","(",")",")",")",")",")","(",")","(",")",")",")","("],[")","(","(","(",")","(",")",")","(",")","(",")","(","(",")","(","(",")","(","(",")"],["(",")","(",")",")","(","(",")","(",")","(",")",")",")","(","(","(","(",")","(",")"],["(","(",")","(",")",")","(","(","(",")","(",")","(","(",")",")","(","(","(",")",")"],["(","(","(","(",")",")","(",")","(","(","(",")",")","(",")","(",")",")",")",")","("],["(","(","(",")",")",")","(",")",")","(",")",")","(","(",")","(",")","(","(","(",")"],[")",")",")",")",")",")","(",")",")",")","(","(",")","(",")","(","(","(","(",")",")"]]], False)