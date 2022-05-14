#
# @lc app=leetcode id=12 lang=python3
#
# [12] Integer to Roman
#

# @lc code=start


class Solution:
    def intToRoman(self, num: int) -> str:
        s = ''
        thousands = num // 1000
        s += 'M' * thousands
        num %= 1000
        hundreds = num // 100
        if hundreds == 9:
            s += 'CM'
        else:
            if hundreds >= 5:
                s += 'D'
                hundreds -= 5
            if hundreds == 4:
                s += 'CD'
            else:
                s += 'C' * hundreds
        num %= 100
        tens = num // 10
        if tens == 9:
            s += 'XC'
        else:
            if tens >= 5:
                s += 'L'
                tens -= 5
            if tens == 4:
                s += 'XL'
            else:
                s += 'X' * tens
        num %= 10
        if num == 9:
            s += 'IX'
        else:
            if num >= 5:
                s += 'V'
                num -= 5
            if num == 4:
                s += 'IV'
            else:
                s += 'I' * num
        
        return s
# @lc code=end

from test_utils import run_test

method = Solution().intToRoman
run_test(method, args=[3], expected='III')
run_test(method, args=[58], expected='LVIII')
run_test(method, args=[1994], expected='MCMXCIV')
