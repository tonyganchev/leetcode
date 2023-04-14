from typing import List

#
# @lc app=leetcode id=136 lang=python3
#
# [136] Single Number
#

# @lc code=start

class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        bm = [0 for i in range(0, 60001)]
        for n in nums:
            bm[n + 30000] += 1
        for i in range(len(bm)):
            if bm[i] == 1:
                return i - 30000

# @lc code=end

Solution().singleNumber([2, 2, 1])
