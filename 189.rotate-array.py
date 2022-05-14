#
# @lc app=leetcode id=189 lang=python3
#
# [189] Rotate Array
#

# @lc code=start
from typing import List


class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        for i in range(0, k):
            nums.insert(0, nums.pop())
        
# @lc code=end

from test_utils import run_test


def test(args, k):
    Solution().rotate(args, k)
    return args

method = test
run_test(method, args=[[1,2,3,4,5,6,7], 3], expected=[5,6,7,1,2,3,4])
run_test(method, args=[[-1,-100,3,99], 2], expected=[3,99,-1,-100])