#
# @lc app=leetcode id=887 lang=python3
#
# [887] Super Egg Drop
#

# @lc code=start
class Solution:
    def superEggDrop(self, k: int, n: int) -> int:
        if n == 1:
            return 1
        if k > 1:
            t = 0
            bs = k - 1
            while bs > 0:
                n //= 2
                bs -= 1
                t += 1
                if n == 1:
                    return t
            return t + n - 1
        return n
# @lc code=end

from test_utils import run_test

method = Solution().superEggDrop

run_test(method, [1, 2], 2)
run_test(method, [2, 6], 3)
run_test(method, [3, 14], 4)
run_test(method, [1, 3], 3)
run_test(method, [2, 1], 1)
run_test(method, [2, 2], 2)
