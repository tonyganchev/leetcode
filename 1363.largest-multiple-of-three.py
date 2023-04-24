#
# @lc app=leetcode id=1363 lang=python3
#
# [1363] Largest Multiple of Three
#

# @lc code=start
from typing import List
from functools import cache

class Solution:
    def largestMultipleOfThree(self, digits: List[int]) -> str:
        s = sum(digits)
        digits.sort()
        m = s % 3
        start_idx = 0
        while start_idx < len(digits) and digits[start_idx] == 0:
            start_idx += 1
        if start_idx == len(digits):
            return '0'
        if m == 0:
            return ''.join(str(d) for d in sorted(digits, reverse = True))
        # find the minimum number of digits that when removed lead to a multiple of three
        self.digits = digits
        for l in range(1, len(self.digits)):
            r = self.find_best_to_remove(start_idx, l, m, 0)
            if r is not None:
                for d in r:
                    self.digits.remove(d)
                if start_idx == len(self.digits):
                    return '0'
                return ''.join([str(s) for s in  sorted(digits, reverse=True)])
        return ''

    @cache
    def find_best_to_remove(self, start_index, length, mod, s):
        for i in range(start_index, len(self.digits) - length + 1):
            if length == 1:
                if (s + self.digits[i]) % 3 == mod:
                    return [self.digits[i]]
            else:
                r = self.find_best_to_remove(i + 1, length - 1, mod, s + self.digits[i])
                if r is not None:
                    return [self.digits[i]] + r
        return None


# @lc code=end

from test_utils import run_test

def test(d):
    return Solution().largestMultipleOfThree(d)
method = test

run_test(method, [[8,1,9]], '981')
run_test(method, [[8,6,7,1,0]], '8760')
run_test(method, [[1]], '')
run_test(method, [[0,0,0,0,0,0]], '0')
run_test(method, [[9,8,6,8,6]], '966')
run_test(method, [[0,0,0,0,0,1]], '0')
