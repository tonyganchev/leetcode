#
# @lc app=leetcode id=2248 lang=python3
#
# [2248] Intersection of Multiple Arrays
#

# @lc code=start
from typing import List



class Solution:
    def intersection(self, nums: List[List[int]]) -> List[int]:
        ns = set(nums[0])
        for na in nums:
            ns2 = set()
            for n in na:
                if n in ns:
                    ns2.add(n)
            ns = ns2
        return sorted([n for n in ns])



# @lc code=end

from test_utils import run_test
run_test(Solution().intersection, args=[[[3,1,2,4,5],[1,2,3,4],[3,4,5,6]]], expected=[3,4])
run_test(Solution().intersection, args=[[[1,2,3],[4,5,6]]], expected=[])