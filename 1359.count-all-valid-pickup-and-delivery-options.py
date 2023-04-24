#
# @lc app=leetcode id=1359 lang=python3
#
# [1359] Count All Valid Pickup and Delivery Options
#

# @lc code=start

from functools import cache

class Solution:
    def countOrders(self, n: int) -> int:
        return self.solve(n, 0)

    @cache
    def solve(self, ps: int, ds: int):
        if ps + ds == 0:
            return 1
        else:
            v = 0
            if ps > 0:
                v += ps * self.solve(ps - 1, ds + 1)
            if ds > 0:
                v += ds * self.solve(ps, ds - 1)
            v  %= 1000000007
            return v

# @lc code=end

from test_utils import run_test

def test(n):
    return Solution().countOrders(n)
method = test

run_test(method, [1], 1)
run_test(method, [2], 6)
run_test(method, [3], 90)
run_test(method, [6], 7484400)
run_test(method, [8], 729647433)
run_test(method, [9], 636056472)
run_test(method, [10], 850728840)
run_test(method, [11], 518360668)
run_test(method, [12], 67543367)
run_test(method, [13], 951594128)
run_test(method, [14], 702577871)
run_test(method, [15], 621371750)
run_test(method, [16], 200385844)
run_test(method, [17], 416457700)
run_test(method, [18], 368349166)
run_test(method, [50], 784760423)
run_test(method, [100], 14159051)
run_test(method, [200], 880584563)
run_test(method, [300], 880584563)
run_test(method, [400], 880584563)
run_test(method, [500], 880584563)
