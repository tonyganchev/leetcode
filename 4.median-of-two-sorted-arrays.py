#
# @lc app=leetcode id=4 lang=python3
#
# [4] Median of Two Sorted Arrays
#

from typing import List

# @lc code=start
class Solution:
    def findMedianSortedArrays(self, a: List[int], b: List[int]) -> float:
        r = a
        r.extend(b)
        r.sort()
        l = len(r)
        if l % 2 == 0:
            return (r[l // 2 - 1] + r[l // 2]) / 2.0
        return r[l // 2]

# @lc code=end

from test_utils import run_test

def test (a, b):
    return Solution().findMedianSortedArrays(a, b)
method = test

run_test(method, [[1, 3], [2]], 2)
run_test(method, [[1, 2], [3, 4]], 2.5)
