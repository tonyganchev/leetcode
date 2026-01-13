#
# @lc app=leetcode id=69 lang=python3
#
# [69] Sqrt(x)
#

# @lc code=start
class Solution:
    def mySqrt(self, x: int) -> int:
        if x < 2:
            return x
        
        lo = 1
        hi = x // 2 + 1
        while True:
            if lo == hi:
                return lo
            mid = (hi + lo) // 2 + 1
            if mid * mid == x:
                return mid
            elif mid * mid > x:
                hi = mid - 1
            else:
                lo = mid
                
        
        for i in range(0, x // 2 + 2):
            if i * i > x:
                return i - 1
        assert False, "mizerie"
# @lc code=end

from test_utils import run_test

def test(x):
    return Solution().mySqrt(x)

method = test

run_test(method, [0], 0)
run_test(method, [1], 1)
run_test(method, [2], 1)
run_test(method, [3], 1)
run_test(method, [4], 2)
run_test(method, [5], 2)
run_test(method, [6], 2)
run_test(method, [7], 2)
run_test(method, [8], 2)
run_test(method, [9], 3)
run_test(method, [10], 3)
run_test(method, [11], 3)
run_test(method, [12], 3)
run_test(method, [13], 3)
run_test(method, [14], 3)
run_test(method, [15], 3)
run_test(method, [16], 4)