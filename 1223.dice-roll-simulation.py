#
# @lc app=leetcode id=1223 lang=python3
#
# [1223] Dice Roll Simulation
#

# @lc code=start
from typing import List


class Solution:
    def dieSimulator(self, n: int, rollMax: List[int]) -> int:
        rollMax.sort()
        variants = 6
        vars = {}
        for i in rollMax:
            variants -= 1
            vars[i] = variants
        print(vars)
        variants = 6
        perms = 1
        for i in range(1, n + 1):
            perms *= variants
            if i in vars:
                variants = vars[i]
        return perms
# @lc code=end

from test_utils import run_test

method = Solution().dieSimulator

run_test(method, [2, [1,1,2,2,2,3]], 34)
run_test(method, [2, [1,1,1,1,1,1]], 30)
run_test(method, [3, [1,1,1,2,2,3]], 101)
