#
# @lc app=leetcode id=67 lang=python3
#
# [67] Add Binary
#

# @lc code=start
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        carry = False
        l, r = (a, b) if len(a) > len(b) else (b, a)
        dl = len(l) - len(r)
        r = '0' * dl + r
        print(l)
        print(r)
        res = ''
        for i in reversed(range(len(l))):
            lc, rc = (l[i], r[i]) if l[i] == '0' else (r[i], l[i])
            if lc == '0':
                if rc == '0':
                    res += ('1' if carry else '0')
                    carry = False
                else:
                    res += ('0' if carry else '1')
            else:
                res += ('1' if carry else '0')
                carry = True
        if carry:
            res += '1'
        return res[::-1]
# @lc code=end

from test_utils import run_test

method = Solution().addBinary

run_test(method, ['11', '1'], '100')
run_test(method, ['1010', '1011'], '10101')
