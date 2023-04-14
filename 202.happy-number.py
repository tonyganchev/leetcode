#
# @lc app=leetcode id=202 lang=python3
#
# [202] Happy Number
#

# @lc code=start
class Solution:
    def isHappy(self, n: int) -> bool:
        h = set([n])
        while True:
            n = self.dsq(n)
            if n == 1:
                return True
            if n in h:
                return False
            h.add(n)
    
    def dsq(self, n: int) -> int:
        nn = 0
        while n > 0:
            nn += (n % 10) ** 2
            n //= 10
        return nn
# @lc code=end
