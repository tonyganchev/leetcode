#
# @lc app=leetcode id=1240 lang=python3
#
# [1240] Tiling a Rectangle with the Fewest Squares
#

# @lc code=start
class Solution:
    def tilingRectangle(self, n: int, m: int) -> int:
        pass
# @lc code=end

from test_utils import run_test

method = Solution().tilingRectangle

run_test(method, [2, 3], 3)
run_test(method, [5, 8], 5)
run_test(method, [11, 13], 6)
