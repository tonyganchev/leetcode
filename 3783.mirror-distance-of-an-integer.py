#
# @lc app=leetcode id=3783 lang=python3
#
# [3783] Mirror Distance of an Integer
#

# @lc code=start
class Solution:
    def mirrorDistance(self, n: int) -> int:
        n0 = n
        r = 0
        while n > 0:
            d = n % 10
            n //= 10
            r = 10 * r + d
        return abs(n0 - r)
# @lc code=end

