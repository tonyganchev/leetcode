#
# @lc app=leetcode id=268 lang=python3
#
# [268] Missing Number
#

# @lc code=start
from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        ns = set(nums)
        i = 0
        while True:
            if i not in ns:
                return i
            i += 1
        assert False
# @lc code=end

from test_utils import run_test

method=Solution().missingNumber
run_test(method, args=[[3, 0, 1]], expected=2)
run_test(method, args=[[0, 1]], expected=2)
run_test(method, args=[[9, 6, 4, 2, 3, 5, 7, 0, 1]], expected=8)
