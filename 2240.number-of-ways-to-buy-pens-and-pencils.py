#
# @lc app=leetcode id=2240 lang=python3
#
# [2240] Number of Ways to Buy Pens and Pencils
#

# @lc code=start
class Solution:
    def waysToBuyPensPencils(self, total: int, cost1: int, cost2: int) -> int:
        ways = 0
        max_pen_count = total // cost1
        for i in range(max_pen_count + 1):
            ways += (total - i * cost1) // cost2 + 1
        return ways
# @lc code=end

from test_utils import run_test

method = Solution().waysToBuyPensPencils
run_test(method, args=[20, 10, 5], expected=9)
run_test(method, args=[5, 10, 10], expected=1)
