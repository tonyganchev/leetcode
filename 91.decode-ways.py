#
# @lc app=leetcode id=91 lang=python3
#
# [91] Decode Ways
#

# @lc code=start
class Solution:
    def __init__(self) -> None:
        self.c = {}

    def numDecodings(self, s: str) -> int:
        if len(s) == 0:
            dc = 1
        elif s[0] == '0':
            dc = 0
        elif len(s) == 1:
            dc = 1
        elif s in self.c:
            dc = self.c[s]
        else:
            dc = self.numDecodings(s[1:])
            if (int(s[0]) == 2 and int(s[1]) <= 6) or int(s[0]) <= 1:
                dc += self.numDecodings(s[2:])
        self.c[s] = dc
        print('{} {}'.format(s, dc))
        return dc

# @lc code=end

method = Solution().numDecodings

from test_utils import run_test

run_test(method, ['111111111111111111111111111111111111111111111',], 1836311903)
