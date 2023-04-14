#
# @lc app=leetcode id=70 lang=python
#
# [70] Climbing Stairs
#

# @lc code=start
class Solution(object):
    def __init__(self):
        self.c = { 0: 0, 1: 1, 2: 2 }
        
    def climbStairs(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n in self.c:
            return self.c[n]
        ways = self.climbStairs(n - 1) + self.climbStairs(n - 2)
        self.c[n] = ways
        print(self.c)
        return ways

# @lc code=end

from test_utils import run_test

def test(arg): return Solution().climbStairs(arg)
method = test

run_test(method, (1,), 1)
run_test(method, (2,), 2)
run_test(method, (3,), 3)
run_test(method, (4,), 5)
run_test(method, (5,), 8)
run_test(method, (6,), 13)

'''
2
 2
  2     222
  1
   1    2211
 1
  2
   1    2121
  1
   2    2112
   1
    1   21111
1
 2
  2
   1    1221
  1
   2    1212
   1
    1   12111
 1
  2
   2    1122
   1
    1   11211
  1
   2
    1   11121
   1
    2   11112
    1
     1  111111
'''