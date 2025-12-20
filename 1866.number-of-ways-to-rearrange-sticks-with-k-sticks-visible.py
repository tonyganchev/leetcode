#
# @lc app=leetcode id=1866 lang=python3
#
# [1866] Number of Ways to Rearrange Sticks With K Sticks Visible
#

from typing import List

# @lc code=start

from functools import cache

class Solution:
    def rearrangeSticks(self, n: int, k: int) -> int:
        @cache
        def dp(n, k):
            if k == 0:
                return 0
            if n == k:
                return 1
            return (dp(n - 1, k - 1) + (n - 1) * dp(n - 1, k)) % (10 ** 9 + 7)

        return dp(n, k)

# @lc code=end

from test_utils import run_test

def test(n, k):
    return Solution().rearrangeSticks(n, k)
method = test

run_test(method, [4, 2], 11) # verified
run_test(method, [2, 1], 1) # verified
run_test(method, [5, 2], 50) # verified
run_test(method, [3, 2], 3) # verified
run_test(method, [5, 5], 1) # verified
run_test(method, [11, 11], 1) # verified
run_test(method, [12, 11], 66) # verified
run_test(method, [13, 11], 2717) # verified
run_test(method, [14, 11], 91091) # verified
run_test(method, [15, 11], 2749747) # verified
run_test(method, [16, 11], 78558480) # verified
run_test(method, [20, 11], 647427950) # verified
run_test(method, [105, 20], 680986848) # verified
