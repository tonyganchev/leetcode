#
# @lc app=leetcode id=66 lang=python3
#
# [66] Plus One
#

# @lc code=start
from typing import List


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        for i in range(len(digits) - 1, -1, -1):
            d = digits[i]
            if d == 9:
                digits[i] = 0
            else:
                digits[i] += 1
                break
        if digits[0] == 0:
            digits.insert(0, 1)
        return digits

# @lc code=end

print(Solution().plusOne([0]))
print(Solution().plusOne([1]))
print(Solution().plusOne([9]))
print(Solution().plusOne([1,9]))
print(Solution().plusOne([4,0]))
print(Solution().plusOne([9]))