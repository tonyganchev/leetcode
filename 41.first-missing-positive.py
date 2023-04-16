#
# @lc app=leetcode id=41 lang=python3
#
# [41] First Missing Positive
#

# @lc code=start
from typing import List
import numpy

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        d = numpy.full((0xFFFFFFF), 0)
        lo = 0xFFFFFFF
        hi = 1
        for n in nums:
            if n > 0:
                d[n // 8] |= 1 << (n % 8)
                lo = min(lo, n)
                hi = max(hi, n)
        if lo > 1:
            return 1
        for i in range(0, (hi + 2) // 8 + 1):
            bm = d[i]
            if bm != 0xFF:
                for n in range(1 if i == 0 else 0, 8):
                    if bm & (1 << n) == 0:
                        return i * 8 + n
# @lc code=end

from test_utils import run_test

method = Solution().firstMissingPositive

run_test(method, [[1,2,0]], 3)
run_test(method, [[3,4,-1,1]], 2)
run_test(method, [[7,8,9,11,12]], 1)
