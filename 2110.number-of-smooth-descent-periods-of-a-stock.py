#
# @lc app=leetcode id=2110 lang=python3
#
# [2110] Number of Smooth Descent Periods of a Stock
#

from typing import List

# @lc code=start
class Solution:

    def count_periods(self, begin: int, end: int) -> int:
        max_len = begin - end + 1
        return int((1.0 + max_len) * max_len / 2.0)

    def getDescentPeriods(self, prices: List[int]) -> int:
        periods = 0
        begin = prices[0]
        end = prices[0]
        for p in prices[1 : ]:
            if end - p == 1:
                end = p
            else:
                periods += self.count_periods(begin, end)
                begin = p
                end = p
        periods += self.count_periods(begin, end)
        return periods

# @lc code=end

from test_utils import run_test

def test(data):
    return Solution().getDescentPeriods(data)
method = test

run_test(method, [[3, 2, 1, 4]], 7)
run_test(method, [[8, 6, 7, 7]], 4)
run_test(method, [[1]], 1)
