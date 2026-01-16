#
# @lc app=leetcode id=168 lang=python3
#
# [168] Excel Sheet Column Title
#

# @lc code=start
class Solution:
    def convertToTitle(self, columnNumber: int) -> str:
        digits = ""
        while columnNumber > 0:
            columnNumber, d = divmod(columnNumber - 1, 26)
            digits += chr(ord('A') + d)
        return digits[ : : -1]
# @lc code=end

from test_utils import run_test

def test(columnNumber):
    return Solution().convertToTitle(columnNumber)

run_test(test, [1], 'A')
run_test(test, [2], 'B')
run_test(test, [26], 'Z')
run_test(test, [27], 'AA')
run_test(test, [52], 'AZ')
run_test(test, [53], 'BA')
run_test(test, [78], 'BZ')
run_test(test, [79], 'CA')
run_test(test, [120], 'DP')
run_test(test, [701], 'ZY')
run_test(test, [703], 'AAA')
run_test(test, [1000], 'ALL')
run_test(test, [10000], 'NTP')
run_test(test, [18000], 'ZPH')
run_test(test, [18200], 'ZWZ')
run_test(test, [18278], 'ZZZ')
run_test(test, [18279], 'AAAA')
run_test(test, [18290], 'AAAL')
run_test(test, [18300], 'AAAV')
run_test(test, [18500], 'AAIN')
run_test(test, [19000], 'ABBT')
run_test(test, [20000], 'ACOF')
run_test(test, [22000], 'AFND')
run_test(test, [30000], 'ARIV')
run_test(test, [50000], 'BUYB')
run_test(test, [100000], 'EQXD')
