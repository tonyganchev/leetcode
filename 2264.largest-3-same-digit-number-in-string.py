#
# @lc app=leetcode id=2264 lang=python3
#
# [2264] Largest 3-Same-Digit Number in String
#

# @lc code=start
from os import curdir


class Solution:
    def largestGoodInteger(self, num: str) -> str:
        bestd = None
        curd = num[0]
        curc = 0
        for d in num:
            if d == curd:
                curc += 1
                if curc == 3:
                    if curd == '9':
                        return '999'
                    if bestd is None or curd > bestd:
                        bestd = curd
            else:
                curd = d
                curc = 1
        return '' if bestd is None else bestd * 3
# @lc code=end

from test_utils import run_test

method = Solution().largestGoodInteger
run_test(method, args=['6777133339'], expected='777')
run_test(method, args=['2300019'], expected='000')
run_test(method, args=['42352338'], expected='')
