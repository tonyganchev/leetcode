#
# @lc app=leetcode id=2239 lang=python3
#
# [2239] Find Closest Number to Zero
#

# @lc code=start


from typing import List


class Solution:
    def findClosestNumber(self, nums: List[int]) -> int:
        closest = nums[0]
        for n in nums:
            if abs(n) < abs(closest):
                closest = n
            elif abs(n) == abs(closest):
                closest = max(closest, n)
        return closest
# @lc code=end

from test_utils import run_test

method = Solution().findClosestNumber
run_test(method, args=[[-4, -2, 1, 4, 8]], expected=1)
run_test(method, args=[[2, -1, 1]], expected=1)
