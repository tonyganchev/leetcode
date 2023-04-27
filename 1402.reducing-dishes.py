#
# @lc app=leetcode id=1402 lang=python3
#
# [1402] Reducing Dishes
#

# @lc code=start
from typing import List

class Solution:
    def maxSatisfaction(self, satisfaction: List[int]) -> int:
        satisfaction.sort()
        best_ltc = 0
        ltc = 0
        s = 0
        for i in reversed(range(len(satisfaction))):
            s += satisfaction[i]
            ltc += s
            if ltc < best_ltc:
                break
            best_ltc = ltc
        return best_ltc
# @lc code=end

from test_utils import run_test

method = Solution().maxSatisfaction

run_test(method, [[-1,-8,0,5,-9]], 14)
run_test(method, [[4,3,2]], 20)
run_test(method, [[-1,-4,-5]], 0)
